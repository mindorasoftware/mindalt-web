function sendQuestion() {
    const question = document.getElementById("question").value;
    fetch("/ask", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({question})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("answer").innerText = data.answer || data.error || "Hata oluştu.";
    })
    .catch(err => {
        document.getElementById("answer").innerText = "Hata oluştu: " + err;
    });
}
