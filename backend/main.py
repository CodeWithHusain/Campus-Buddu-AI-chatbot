# backend/main.py

import os
import logging
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from google.genai import types
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

# ---------- CONFIG ----------

logging.basicConfig(level=logging.INFO)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Set GOOGLE_API_KEY in your environment before running.")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

APP_NAME = "campus_buddy_app"
USER_ID = "web_user"

# ---------- TOOLS & AGENT (PASTE YOUR EXISTING CODE HERE) ----------

# from your notebook: _ensure_lists, set_preferred_name, add_class_schedule, ...
# and campus_buddy_agent = Agent(...)

# EXAMPLE (VERY SHORT) – REPLACE THIS WITH YOUR FULL VERSION
from datetime import date, datetime, timedelta
from typing import List, Dict, Any

SCHEDULE_KEY = "user:schedule"
ASSIGNMENTS_KEY = "user:assignments"
PREFS_KEY = "user:prefs"


def _ensure_lists(tool_context):
    state = tool_context.state
    if SCHEDULE_KEY not in state:
        state[SCHEDULE_KEY] = []
    if ASSIGNMENTS_KEY not in state:
        state[ASSIGNMENTS_KEY] = []
    if PREFS_KEY not in state:
        state[PREFS_KEY] = {}
    return state


def set_preferred_name(name: str, tool_context=None) -> Dict[str, Any]:
    state = _ensure_lists(tool_context)
    state[PREFS_KEY]["name"] = name
    return {
        "status": "success",
        "message": f"Nice to meet you, {name}! I'll remember your name.",
        "saved_name": name,
    }


def add_class_schedule(
    day: str,
    subject: str,
    start_time: str,
    end_time: str,
    location: str = "",
    tool_context=None,
) -> Dict[str, Any]:
    state = _ensure_lists(tool_context)
    entry = {
        "day": day.strip().title(),
        "subject": subject.strip(),
        "start_time": start_time.strip(),
        "end_time": end_time.strip(),
        "location": location.strip(),
    }
    state[SCHEDULE_KEY].append(entry)
    day_count = sum(1 for s in state[SCHEDULE_KEY] if s["day"] == entry["day"])
    return {
        "status": "success",
        "message": f"Added {subject} on {entry['day']} from {start_time} to {end_time}.",
        "classes_for_day": day_count,
    }


def get_today_schedule(tool_context=None) -> Dict[str, Any]:
    state = _ensure_lists(tool_context)
    schedule: List[Dict[str, Any]] = state[SCHEDULE_KEY]
    today_name = date.today().strftime("%A")
    today_classes = [c for c in schedule if c["day"] == today_name]
    if not today_classes:
        return {
            "status": "empty",
            "day": today_name,
            "classes": [],
            "summary": f"No classes saved for {today_name}.",
        }
    today_classes_sorted = sorted(today_classes, key=lambda c: c["start_time"])
    return {
        "status": "success",
        "day": today_name,
        "classes": today_classes_sorted,
        "summary": f"You have {len(today_classes_sorted)} classes on {today_name}.",
    }


def add_assignment(
    course: str,
    title: str,
    due_date: str,
    priority: str = "medium",
    tool_context=None,
) -> Dict[str, Any]:
    state = _ensure_lists(tool_context)
    assignment = {
        "course": course.strip(),
        "title": title.strip(),
        "due_date": due_date.strip(),
        "priority": priority.lower().strip(),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "pending",
    }
    state[ASSIGNMENTS_KEY].append(assignment)
    pending_count = sum(1 for a in state[ASSIGNMENTS_KEY] if a["status"] == "pending")
    return {
        "status": "success",
        "message": f"Added assignment '{title}' for {course} due on {due_date}.",
        "pending_assignments": pending_count,
    }


def list_upcoming_assignments(
    max_days: int = 30,
    tool_context=None,
) -> Dict[str, Any]:
    state = _ensure_lists(tool_context)
    assignments: List[Dict[str, Any]] = state[ASSIGNMENTS_KEY]
    today = date.today()
    upcoming: List[Dict[str, Any]] = []
    for a in assignments:
        try:
            due = datetime.strptime(a["due_date"], "%Y-%m-%d").date()
        except ValueError:
            continue
        if today <= due <= today + timedelta(days=max_days) and a["status"] == "pending":
            days_left = (due - today).days
            aa = dict(a)
            aa["days_left"] = days_left
            upcoming.append(aa)
    upcoming_sorted = sorted(upcoming, key=lambda a: (a["days_left"], a["priority"]))
    if not upcoming_sorted:
        return {
            "status": "empty",
            "assignments": [],
            "summary": f"No pending assignments in the next {max_days} days.",
        }
    return {
        "status": "success",
        "assignments": upcoming_sorted,
        "summary": f"You have {len(upcoming_sorted)} upcoming assignments.",
    }



campus_buddy_agent = Agent(
    model="gemini-2.5-flash",
    name="campus_buddy_agent",
    description="Campus assistant for classes, assignments.",
    instruction=(
        "You are Campus Buddy, a friendly AI agent for college students. "
        "Use tools to manage schedule and assignments, and cheer students up "
       
    ),
    tools=[
        set_preferred_name,
        add_class_schedule,
        get_today_schedule,
        add_assignment,
        list_upcoming_assignments,
        
    ],
)

# ---------- SESSION + RUNNER ----------

session_service = InMemorySessionService()
session = session_service.create_session_sync(app_name=APP_NAME, user_id=USER_ID)
SESSION_ID = session.id

runner = Runner(
    agent=campus_buddy_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

# ---------- FASTAPI APP ----------

app = FastAPI()

# allow frontend (running on another port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev, allow all; tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    user_message = req.message

    content = types.Content(
        role="user",
        parts=[types.Part(text=user_message)],
    )

    final_response: Optional[str] = None

    try:
        for event in runner.run(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=content,
        ):
            # Optional logging of tool calls
            for call in event.get_function_calls():
                logging.info(f"Tool called: {call.name} with args {call.args}")

            if event.is_final_response():
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if getattr(part, "text", None):
                            final_response = part.text
                            break
    except Exception as e:
        logging.error(f"Error while running agent: {e}")
        final_response = "Kuch error aa gaya server side pe. Thodi der baad try karo 🙂"

    if final_response is None:
        final_response = "Hmm, I didn't get any response from the agent."

    return ChatResponse(reply=final_response)
