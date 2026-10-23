# 🎓 Campus Buddy – AI Study & Schedule Assistant

**Campus Buddy** is a full-stack AI-powered assistant designed to help college students organize their academic life. It combines conversational AI with schedule management, assignment tracking, and personalized study planning.

Built using **Google Agent Development Kit (ADK), Gemini, FastAPI, and HTML/CSS/JavaScript**, Campus Buddy provides a simple chat interface for managing everyday academic tasks.

## ✨ Features

- 💬 **Conversational AI** — Interact with Campus Buddy through a natural-language chat interface.
- 🗓️ **Class Schedule Management** — Add classes with their day, time, and location, and ask questions such as *“What classes do I have today?”*
- ✅ **Assignment Tracking** — Record assignments with due dates and priorities, and ask *“Show my upcoming assignments for the next 7 days.”*
- 📚 **Study Planning** — Generate day-wise or exam-oriented study plans.
- 🧠 **Session-Based Memory** — Maintain schedule and assignment data for the current user session using ADK's `session.state`.
- 🌙 **Modern Web Interface** — Use a dark-themed chat UI built with HTML, CSS, and vanilla JavaScript.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.x | Backend development |
| FastAPI | HTTP API and backend services |
| Google ADK | AI agent orchestration |
| Google Gemini API | Language model for conversational interactions |
| `InMemorySessionService` | In-memory session and state management |
| HTML5 and CSS3 | Frontend structure and styling |
| Vanilla JavaScript | Chat interactions and API requests |

## 📁 Project Structure

```text
campus-buddy-web/
├── backend/
│   └── main.py          # FastAPI app, ADK agent, tools and sessions
├── frontend/
│   ├── index.html       # Chat interface
│   ├── styles.css      # UI styling
│   └── app.js           # Frontend interaction logic
└── README.md
```

## 🚀 Getting Started

### Prerequisites

Before running the project, make sure you have:

- Python 3.x installed
- A Google Gemini API key
- Git installed
- A web browser

### 1. Clone the repository

```bash
git clone <YOUR-REPOSITORY-URL>
cd campus-buddy-web
```

Replace `<YOUR-REPOSITORY-URL>` with your repository's clone URL.

### 2. Set up the Python environment

```bash
python -m venv .venv
```

Activate the environment:

**Windows**
```bash
.venv\Scripts\activate
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

Install the packages required by your backend:

```bash
pip install fastapi uvicorn google-adk
```

If your project uses additional packages, install those too. A `requirements.txt` file is recommended for reproducible setup.

### 4. Configure your Gemini API key

Set your API key as an environment variable rather than hardcoding it in your source code.

**Windows PowerShell**
```powershell
$env:GOOGLE_API_KEY="your-api-key"
```

**macOS / Linux**
```bash
export GOOGLE_API_KEY="your-api-key"
```

Replace `your-api-key` with your actual key. Do not commit API keys or other secrets to GitHub.

### 5. Start the backend

From the project root, run:

```bash
uvicorn backend.main:app --reload
```

This command assumes `backend/main.py` exposes a FastAPI instance named `app` and that the project is importable from the root directory. Adjust it if your entry point differs.

### 6. Open the frontend

Open `frontend/index.html` in your browser, or serve the frontend using a local development server if your app requires one.

Make sure the API URL configured in `frontend/app.js` matches the address where your FastAPI backend is running.

## 💡 Example Prompts

Try asking Campus Buddy:

- “What classes do I have today?”
- “Add my mathematics class on Monday at 10 AM.”
- “Show my assignments due in the next 7 days.”
- “Which assignment should I prioritize first?”
- “Create a study plan for my upcoming exams.”
- “Help me make a study timetable for tomorrow.”

*The exact commands supported depend on the tools and functionality implemented in the backend.*

## 🧠 How It Works

1. **User interaction:** The student sends a message through the web chat interface.
2. **API request:** The frontend sends the message to the FastAPI backend.
3. **Agent processing:** The Google ADK agent interprets the request and uses Gemini to help generate a response.
4. **State management:** Session state stores relevant schedule and assignment data for the active session.
5. **Response delivery:** The backend returns the response to the frontend, where it appears in the chat.

## 🔒 Data and Session Management

Campus Buddy uses `InMemorySessionService` and ADK's `session.state` to manage session-related information.

Because this is an in-memory approach, data should **not be assumed to persist after a server restart**. It is suitable for a prototype or local demonstration, but persistent storage and appropriate access controls would be needed for a production deployment.

## 🛣️ Future Improvements

- [ ] Persistent storage for classes and assignments
- [ ] Calendar integration and reminders
- [ ] User authentication and individual student accounts
- [ ] Exam timetable import and automatic study scheduling
- [ ] Assignment deadline notifications
- [ ] Responsive design improvements for mobile devices
- [ ] Automated tests for backend tools and API endpoints

## 🤝 Contributing

Contributions, suggestions, and bug reports are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make and test your changes.
4. Commit your changes with a descriptive message.
5. Open a pull request describing your contribution.

## 📄 License

No license has been specified yet. Add a `LICENSE` file and update this section if you decide to distribute the project under an open-source license.

---

**Built to make student life more organized, one conversation at a time.** 🎓
