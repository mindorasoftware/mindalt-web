const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const chatContainer = document.getElementById("chat-container");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = input.value.trim();
    if (!message) return;

    // Kullanıcının mesajını göster
    addMessage(message, "user");
    input.value = "";

    try {
        const res = await fetch("https://mindalt-web-1-0.onrender.com/api", {  // canlı URL
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await res.json();
        if (data.answer) {
            addMessage(data.answer, "bot");  // GPT cevabı
        } else {
            addMessage("Bir hata oluştu...", "bot");
        }
    } catch (err) {
        addMessage("Bir hata oluştu...", "bot");
    }
});

function addMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = `message ${sender}`;
    msg.textContent = text;
    chatContainer.appendChild(msg);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
