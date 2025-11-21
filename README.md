# 🎓 Campus Buddy – AI Study & Schedule Assistant

Campus Buddy is a full-stack AI assistant for college students.  
It helps you manage:

- 🧾 Class schedules  
- ✅ Assignments & deadlines  
- 📚 Exam prep & study plans  

Built with **Google Agent Development Kit (ADK)**, **Gemini**, **FastAPI**, and a custom **chat UI** in HTML/CSS/JavaScript.

---

## ✨ Key Features

- **Chat-based interface** – talk to Campus Buddy like a normal chatbot.
- **Class schedule management**
  - Add classes with day, time and location.
  - Ask: _“What classes do I have today?”_
- **Assignment tracking**
  - Add assignments with due dates and priority.
  - Ask: _“Show my upcoming assignments for the next 7 days.”_
- **Study planning**
  - Ask for day-wise or exam-wise study plans.
- **Session memory**
  - Stores schedule and assignments for the current user session using ADK’s `session.state`.
- **Web UI**
  - Dark, app-like chat interface inspired by modern AI tools.

---

## 🏗️ Tech Stack

**Backend**

- Python 3.x  
- [FastAPI](https://fastapi.tiangolo.com/) – HTTP API  
- [Google ADK](https://github.com/google/adk-python) – Agent orchestration  
- [Google Gemini API](https://ai.google.dev/) – LLM  
- `InMemorySessionService` – simple session + state store

**Frontend**

- HTML5 + CSS3 (custom styling)  
- Vanilla JavaScript (fetch API → FastAPI backend)

---

## 📁 Project Structure

```text
campus-buddy-web/
│
├─ backend/
│   └─ main.py          # FastAPI app, ADK agent, tools & session setup
│
├─ frontend/
│   ├─ index.html       # Chat UI layout
│   ├─ styles.css       # Dark theme & layout styling
│   └─ app.js           # Frontend logic (send/receive messages)
├
└─ README.md
