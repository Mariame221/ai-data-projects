from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import webbrowser
from threading import Timer
from ssml_messages import build_ssml
from gtts import gTTS

import re

app = Flask(__name__, static_folder="front", template_folder="front")


# ==============================
# FONCTION AUDIO
# ==============================
def generate_audio_from_ssml(ssml_text, output_path="front/last_voice.mp3"):
    clean_text = re.sub("<[^>]+>", "", ssml_text)  # Nettoyage SSML
    tts = gTTS(clean_text, lang="fr")
    tts.save(output_path)
    print("Audio généré via gTTS :", output_path)
    return output_path


# ==============================
# BASE EMPLOYÉS
# ==============================
EMPLOYES = {
    # --- Employés standards ---
    "EMP-001-ALPHA": {"prenom": "Gloria"},
    "EMP-002-BETA": {"prenom": "Sarah"},
    "EMP-003-GAMMA": {"prenom": "Ousmane"},
    "EMP-004-DELTA": {"prenom": "Fatou"},

    # --- Boss / Direction ---
    "BOSS-001": {"prenom": "Madame Bah", "is_boss": True},
    "BOSS-002": {"prenom": "Monsieur Diallo", "is_boss": True},

    # --- Anniversaire ---
    "EMP-ANNIV-001": {"prenom": "Stébou", "anniversaire": True},
    "EMP-ANNIV-002": {"prenom": "Moussa", "anniversaire": True},

    # --- Retard ---
    "RETARD-001": {"prenom": "Penda", "retard": 12},
    "RETARD-002": {"prenom": "Abdou", "retard": 25},

    # --- Avance ---
    "AVANCE-001": {"prenom": "Mariama", "avance": 15},

    # --- Absence ---
    "ABS-001": {"prenom": "Cheikh", "absent": True},

    # --- Télétravail ---
    "REMOTE-001": {"prenom": "Awa", "remote": True},

    # --- Pause ---
    "BREAK-001": {"prenom": "Ibrahima", "pause": True},

    # --- Réunion ---
    "MEET-001": {"prenom": "Seynabou", "meeting": "10h00"},
    "MEET-002": {"prenom": "Mamadou", "meeting": "14h30"},

    # --- Formation ---
    "FORM-001": {"prenom": "Khadija", "formation": "Sécurité incendie"},

    # --- Congés ---
    "OFF-001": {"prenom": "Ndeye", "conges": True},

    # --- Avertissement ---
    "WARN-001": {"prenom": "Alioune", "avertissement": True},

    # --- VIP ---
    "VIP-001": {"prenom": "Samba", "vip": True},

    # --- Refus ---
    "REFUS-001": {"prenom": "Inconnu", "refus": True},

    # --- Debug ---
    "TEST-VOICE": {"prenom": "Test", "debug": True}
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

    # Extraction des infos
    ssml_message = build_ssml(
        prenom=employe.get("prenom"),
        retard=employe.get("retard", 0),
        avance=employe.get("avance", 0),
        is_boss=employe.get("is_boss", False),
        anniversaire=employe.get("anniversaire", False),
        refus=employe.get("refus", False),
        absent=employe.get("absent", False),
        remote=employe.get("remote", False),
        pause=employe.get("pause", False),
        meeting=employe.get("meeting"),
        formation=employe.get("formation"),
        conges=employe.get("conges", False),
        avertissement=employe.get("avertissement", False),
        vip=employe.get("vip", False),
        status=data.get("status", "normal")
    )

    print("=== SSML GÉNÉRÉ ===\n")
    print(ssml_message)
    print("\n===================")

    generate_audio_from_ssml(ssml_message)

    return jsonify({
        "message": f"Message généré pour {employe.get('prenom')}",
        "audio": "/audio/last_voice.mp3"
    })


# ==============================
# OUVERTURE AUTOMATIQUE DU NAVIGATEUR
# ==============================
def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=True)
