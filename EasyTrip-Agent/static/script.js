const messagesEl = document.getElementById("messages");
const formEl = document.getElementById("chat-form");
const inputEl = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");

const history = [];

function appendMessage(role, content, extraClass = "") {
  const row = document.createElement("div");
  row.className = `message ${role}`;

  const bubble = document.createElement("div");
  bubble.className = `bubble ${extraClass}`.trim();
  bubble.textContent = content;

  row.appendChild(bubble);
  messagesEl.appendChild(row);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return bubble;
}

function setLoading(isLoading) {
  sendBtn.disabled = isLoading;
  inputEl.disabled = isLoading;
}

function autoResize() {
  inputEl.style.height = "auto";
  inputEl.style.height = `${Math.min(inputEl.scrollHeight, 140)}px`;
}

inputEl.addEventListener("input", autoResize);

inputEl.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    formEl.requestSubmit();
  }
});

formEl.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = inputEl.value.trim();
  if (!message) return;

  appendMessage("user", message);
  history.push({ role: "user", content: message });
  inputEl.value = "";
  autoResize();

  const typing = appendMessage("assistant", "Thinking...", "typing");
  setLoading(true);

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, history }),
    });

    const data = await response.json();
    typing.remove();

    if (!response.ok) {
      appendMessage("assistant", data.error || "Something went wrong.", "error");
      return;
    }

    appendMessage("assistant", data.reply);
    history.push({ role: "assistant", content: data.reply });
  } catch (error) {
    typing.remove();
    appendMessage("assistant", `Network error: ${error.message}`, "error");
  } finally {
    setLoading(false);
    inputEl.focus();
  }
});

inputEl.focus();
