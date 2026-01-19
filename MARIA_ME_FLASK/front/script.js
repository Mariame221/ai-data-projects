const scanBtn = document.getElementById("scan-btn");
const qrInput = document.getElementById("qr");
const loader = document.getElementById("loader");
const responseText = document.getElementById("response-text");
const errorBox = document.getElementById("error");
const scanSound = document.getElementById("scan-sound");

const speakBtn = document.getElementById("speak-btn");
const voice = document.getElementById("voice");
const avatar = document.querySelector(".ai-avatar");

const API_URL = "/scan";

scanBtn.addEventListener("click", handleScan);
qrInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") handleScan();
});

async function handleScan() {
    const qr = qrInput.value.trim();

    errorBox.classList.add("hidden");
    errorBox.textContent = "";

    if (!qr) {
        showError("Merci de renseigner un QR code valide.");
        return;
    }

    try {
        scanSound.currentTime = 0;
        scanSound.play();
    } catch {}

    loader.classList.remove("hidden");
    responseText.textContent = "";

    try {
        const res = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ qr: qr })
        });

        const data = await res.json();

        if (!res.ok) {
            showError(data.detail || "Erreur inconnue.");
            return;
        }

        responseText.textContent = data.message;

        if (data.audio) {
            const audio = new Audio(data.audio + "?t=" + Date.now());
            audio.play();
        }

    } catch {
        showError("Impossible de contacter mar‑IA‑me.");
    } finally {
        loader.classList.add("hidden");
    }
}

function showError(msg) {
    errorBox.textContent = msg;
    errorBox.classList.remove("hidden");
}

speakBtn.addEventListener("click", () => {
    avatar.classList.add("talking");
    voice.currentTime = 0;

    voice.play().catch(() => {
        avatar.classList.remove("talking");
    });

    voice.onended = () => avatar.classList.remove("talking");
});
