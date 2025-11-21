// frontend/app.js

const API_URL = "http://127.0.0.1:8000/chat"; // change if backend is elsewhere

const chatContainer = document.getElementById("chat-container");
const input = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");
const suggestBtn = document.getElementById("suggest-btn");

let isSending = false;

const SUGGESTIONS = [
  "Plan my study schedule for today. I have COA, DSA and Maths.",
  "Show my upcoming assignments for the next 7 days.",
  "What classes do I have today?",
  "I'm stressed about exams, give me a short shayari.",
];

function addMessage({ sender, text }) {
  const row = document.createElement("div");
  row.className = `message-row ${sender === "bot" ? "bot" : "user"}`;

  if (sender === "bot") {
    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = "CB";
    row.appendChild(avatar);
  }

  const bubble = document.createElement("div");
  bubble.className = `message-bubble ${sender === "bot" ? "bot" : "user"}`;

  if (sender === "bot") {
    const meta = document.createElement("div");
    meta.className = "message-meta";
    meta.textContent = "Campus Buddy";
    bubble.appendChild(meta);
  }

  const textEl = document.createElement("div");
  textEl.textContent = text;
  bubble.appendChild(textEl);

  row.appendChild(bubble);
  chatContainer.appendChild(row);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addTypingIndicator() {
  const row = document.createElement("div");
  row.className = "message-row bot";
  row.id = "typing-row";

  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  avatar.textContent = "CB";

  const bubble = document.createElement("div");
  bubble.className = "message-bubble bot";

  const indicator = document.createElement("div");
  indicator.className = "typing-indicator";
  indicator.innerHTML = `
    <span>Typing</span>
    <span class="typing-dot"></span>
    <span class="typing-dot"></span>
    <span class="typing-dot"></span>
  `;

  bubble.appendChild(indicator);
  row.appendChild(avatar);
  row.appendChild(bubble);

  chatContainer.appendChild(row);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function removeTypingIndicator() {
  const row = document.getElementById("typing-row");
  if (row) row.remove();
}

async function sendMessage() {
  const text = input.value.trim();
  if (!text || isSending) return;

  isSending = true;
  input.value = "";

  addMessage({ sender: "user", text });
  addTypingIndicator();

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: text }),
    });

    const data = await res.json();
    removeTypingIndicator();

    if (data && data.reply) {
      addMessage({ sender: "bot", text: data.reply });
    } else {
      addMessage({
        sender: "bot",
        text: "Hmm, I didn't get a proper reply from the server.",
      });
    }
  } catch (err) {
    console.error(err);
    removeTypingIndicator();
    addMessage({
      sender: "bot",
      text: "Network error while talking to server. Check if backend is running.",
    });
  } finally {
    isSending = false;
    input.focus();
  }
}

function insertSuggestedPrompt() {
  const randomPrompt =
    SUGGESTIONS[Math.floor(Math.random() * SUGGESTIONS.length)];
  input.value = randomPrompt;
  input.focus();
}

// Event listeners
sendBtn.addEventListener("click", sendMessage);

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    sendMessage();
  }
});

suggestBtn.addEventListener("click", insertSuggestedPrompt);

// Initial welcome bot message
addMessage({
  sender: "bot",
  text:
    "Hey! I'm Campus Buddy 👋. I can help you with classes, assignments, " +
    "exam prep and more. What do you want to plan today?",
});
