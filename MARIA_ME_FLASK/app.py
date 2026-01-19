from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import webbrowser
from threading import Timer
from ssml_messages import build_ssml
from gtts import gTTS
import re

app = Flask(__name__, static_folder="front", template_folder="front")




def generate_audio_from_ssml(ssml_text, output_path="front/last_voice.mp3"):
    # Nettoyage du SSML → texte simple
    clean_text = re.sub("<[^>]+>", "", ssml_text)

    # Génération audio Google TTS
    tts = gTTS(clean_text, lang="fr")
    tts.save(output_path)

    print("Audio généré via gTTS :", output_path)
    return output_path

# ==============================
# BASE EMPLOYÉS
# ==============================
EMPLOYES = {
    "EMP-001-ALPHA": {"prenom": "Gloria", "is_boss": False},
    "EMP-002-BETA": {"prenom": "Sarah", "is_boss": False},
    "BOSS-001": {"prenom": "Madame Bah", "is_boss": True},
    "EMP-ANNIV": {"prenom": "stébou", "is_boss": False, "anniversaire": True},
    "REFUS-001": {"prenom": "Inconnu", "is_boss": False, "refus": True},
    "RETARD-001": {"prenom": "penda", "is_boss": False, "retard": 12}
}


# ==============================
# ROUTES
# ==============================
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/audio/<filename>")
def audio(filename):
    return send_from_directory("front", filename)


@app.route("/scan", methods=["POST"])
def scan():
    data = request.json
    qr = data.get("qr")

    if not qr:
        return jsonify({"detail": "QR code manquant"}), 400

    if qr not in EMPLOYES:
        return jsonify({"detail": "Employé inconnu"}), 400

    employe = EMPLOYES[qr]
    prenom = employe.get("prenom")
    is_boss = employe.get("is_boss", False)
    retard = employe.get("retard", 0)
    anniversaire = employe.get("anniversaire", False)
    refus = employe.get("refus", False)

    status = data.get("status", "normal")

    # Génération du SSML
    ssml_message = build_ssml(
        prenom=prenom,
        retard=retard,
        is_boss=is_boss,
        anniversaire=anniversaire,
        refus=refus,
        status=status
    )

    print("=== SSML GÉNÉRÉ ===")
    print(ssml_message)
    print("===================")

    # Génération audio locale
    generate_audio_from_ssml(ssml_message)

    return jsonify({
        "message": f"Message généré pour {prenom}",
        "audio": "/audio/last_voice.mp3"
    })


# ==============================
# AUTO-OUVERTURE DU NAVIGATEUR
# ==============================
def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=True)
