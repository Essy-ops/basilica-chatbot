// BASILICA frontend logic — talks to the deployed Flask API on Render

const API_URL = "https://basilica-chatbot.onrender.com/ask";

const chat = document.getElementById("chat");
const form = document.getElementById("chatForm");
const input = document.getElementById("questionInput");
const sendBtn = document.getElementById("sendBtn");
const statusBanner = document.getElementById("statusBanner");

function addBubble(text, sender, meta) {
  const b = document.createElement("div");
  b.className = "bubble " + sender;
  b.textContent = text;
  if (meta) {
    const m = document.createElement("div");
    m.className = "meta";
    m.textContent = meta;
    b.appendChild(m);
  }
  chat.appendChild(b);
  chat.scrollTop = chat.scrollHeight;
  return b;
}

function showTyping() {
  const t = document.createElement("div");
  t.className = "typing";
  t.id = "typingIndicator";
  t.innerHTML = "<span></span><span></span><span></span>";
  chat.appendChild(t);
  chat.scrollTop = chat.scrollHeight;
}

function hideTyping() {
  const t = document.getElementById("typingIndicator");
  if (t) t.remove();
}

async function ask(question) {
  if (!question || !question.trim()) return;
  addBubble(question, "user");
  input.value = "";
  sendBtn.disabled = true;
  showTyping();

  const wakeTimer = setTimeout(() => { statusBanner.style.display = "block"; }, 4000);

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const data = await res.json();
    hideTyping();
    clearTimeout(wakeTimer);
    statusBanner.style.display = "none";

    const meta = data.intent
      ? `Matched: ${data.intent} · ${(data.confidence * 100).toFixed(0)}% confident`
      : `Not confident enough to answer directly`;
    addBubble(data.answer || "Sorry, something went wrong.", "bot", meta);
  } catch (err) {
    hideTyping();
    clearTimeout(wakeTimer);
    statusBanner.style.display = "none";
    addBubble("I couldn't reach the server. Please check your connection and try again.", "bot");
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  ask(input.value);
});
