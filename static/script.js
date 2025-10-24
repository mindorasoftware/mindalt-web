async function sendMessage() {
  const userInput = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");
  const userMessage = userInput.value.trim();

  if (!userMessage) return;

  // Kullanıcı mesajını ekle
  addMessage("Kullanıcı", userMessage);
  userInput.value = "";

  // MindAlt yanıt bekleniyor animasyonu
  const loadingMessage = addMessage("MindAlt", "...");
  loadingMessage.classList.add("loading");

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userMessage }),
    });

    const data = await response.json();
    loadingMessage.remove();

    if (data.reply) {
      addMessage("MindAlt", data.reply);
    } else {
      addMessage("MindAlt", "Bir hata oluştu, lütfen tekrar dene.");
    }
  } catch (error) {
    console.error("Hata:", error);
    loadingMessage.remove();
    addMessage("MindAlt", "Bir bağlantı hatası oluştu.");
  }
}

function addMessage(sender, text) {
  const chatBox = document.getElementById("chat-box");
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", sender.toLowerCase());
  messageDiv.textContent = `${sender}: ${text}`;
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
  return messageDiv;
}

// Enter tuşuyla mesaj gönderme
document.getElementById("user-input").addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

// Buton tıklamayla mesaj gönderme
document.getElementById("send-btn").addEventListener("click", sendMessage);
