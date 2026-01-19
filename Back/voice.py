from gtts import gTTS

def speak(text: str):
    try:
        tts = gTTS(text=text, lang="fr")
        filename = "last_voice.mp3"
        tts.save(filename)
        return filename
    except Exception as e:
        print("Erreur synthèse vocale :", e)
        return None
