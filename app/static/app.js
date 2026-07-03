const form = document.querySelector("#chatForm");
const promptInput = document.querySelector("#prompt");
const messages = document.querySelector("#messages");
const sendButton = document.querySelector("#sendButton");
const clearButton = document.querySelector("#clearChat");

function addMessage(text, role, extraClass = "") {
  const article = document.createElement("article");
  article.className = `message ${role} ${extraClass}`.trim();

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  article.appendChild(bubble);
  messages.appendChild(article);
  messages.scrollTop = messages.scrollHeight;
  return article;
}

function resizeInput() {
  promptInput.style.height = "auto";
  promptInput.style.height = `${Math.min(promptInput.scrollHeight, 150)}px`;
}

async function sendPrompt(prompt) {
  const response = await fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ prompt }),
  });

  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(payload.detail || "Request failed");
  }

  return payload.response;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const prompt = promptInput.value.trim();
  if (!prompt) {
    return;
  }

  addMessage(prompt, "user");
  promptInput.value = "";
  resizeInput();
  promptInput.focus();

  sendButton.disabled = true;
  const typing = addMessage("Thinking...", "bot", "typing");

  try {
    const reply = await sendPrompt(prompt);
    typing.remove();
    addMessage(reply || "No response text returned.", "bot");
  } catch (error) {
    typing.remove();
    addMessage(error.message || "Something went wrong.", "bot", "error");
  } finally {
    sendButton.disabled = false;
  }
});

promptInput.addEventListener("input", resizeInput);

promptInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});

clearButton.addEventListener("click", () => {
  messages.innerHTML = "";
  addMessage("Hi. Send a prompt and I will reply here.", "bot");
  promptInput.focus();
});
