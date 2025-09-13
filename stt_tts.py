# stt_tts.py
import speech_recognition as sr
import pyttsx3
import threading

class LocalSTT:
    def __init__(self, language="en-IN"):
        self.recognizer = sr.Recognizer()
        self.language = language

    def listen_from_mic(self, timeout=5, phrase_time_limit=8):
        with sr.Microphone() as source:
            print("Listening (speak now)...")
            audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
            return text
        except sr.UnknownValueError:
            return ""
        except Exception as e:
            print("STT error:", e)
            return ""

class LocalTTS:
    def __init__(self):
        self.engine = pyttsx3.init()
        # configure voice if desired
        self.lock = threading.Lock()

    def speak(self, text):
        # run speech on another thread to avoid blocking if desired
        with self.lock:
            self.engine.say(text)
            self.engine.runAndWait()

# simple combined helper
stt = LocalSTT()
tts = LocalTTS()
