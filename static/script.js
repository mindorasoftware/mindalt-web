const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const chatContainer = document.getElementById("chat-container");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const userMessage = input.value.trim();
    if (!userMessage) return;

    // Kullanıcı mesajını ekle
    const userDiv = document.createElement("div");
    userDiv.className = "message user";
    userDiv.textContent = userMessage;
    chatContainer.appendChild(userDiv);

    // Cevap baloncuğunu oluştur
    const botDiv = document.createElement("div");
    botDiv.className = "message bot";
    botDiv.textContent = "⌛"; // başlangıçta animasyon yerine simge
    chatContainer.appendChild(botDiv);

    input.value = "";
    chatContainer.scrollTop = chatContainer.scrollHeight;

    // Backend'e POST isteği
    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt: userMessage })
        });

        const data = await response.json();
        botDiv.textContent = data.answer; // cevabı ekrana yaz
        chatContainer.scrollTop = chatContainer.scrollHeight;
    } catch (err) {
        botDiv.textContent = "Bir hata oluştu...";
        console.error(err);
    }
});
