import pyttsx3
import threading
import speech_recognition as sr

# Initialize once
engine = pyttsx3.init('sapi5')
lock = threading.Lock()

def speak(text):
    """Convert text to speech safely."""
    if not text:
        return
    with lock:
        try:
            engine.stop()  # clear any queued speech
            engine.say(str(text))
            engine.runAndWait()
        except RuntimeError:
            # Reinitialize engine if it got stuck
            global engine
            engine = pyttsx3.init('sapi5')
            engine.say(str(text))
            engine.runAndWait()

def listen() -> str:
    """Listen from microphone and return recognized text in Hindi."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="hi-IN")
            print("✅ Recognized:", text)
            return text
        except sr.UnknownValueError:
            return "Maaf kijiye, main aapki baat samajh nahi paaya."
        except sr.RequestError:
            return "Speech service kaam nahi kar raha hai."
