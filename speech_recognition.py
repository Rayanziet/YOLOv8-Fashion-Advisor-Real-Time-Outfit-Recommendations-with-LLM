import speech_recognition as sr
import pyttsx3

class SpeechHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.event_dict = {
            "wedding": "formal",
            "party": "casual",
            "interview": "formal",
            "work": "professional",
            "birthday": "casual",
            "presentation": "business formal",
            "gala": "formal",
            "concert": "casual",
            "vacation": "casual",
            "meeting": "professional"
        }

    def speak_text(self, command):
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()

    def get_event_from_speech(self, timeout=10, time_limit=30):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Calibrated, you may speak now.")
            
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=time_limit)
                text = self.recognizer.recognize_google(audio).lower()
                print("Did you say:", text)
                self.speak_text(text)
                return text, self.classify_event(text)
            
            except sr.RequestError as e:
                print("Couldn't request result:", str(e))
                return None, None
            except sr.UnknownValueError:
                print("Unknown Error occurred")
                return None, None

    def classify_event(self, text):
        for event, event_type in self.event_dict.items():
            if event in text:
                print(f"The clothing type for this event is {event_type}")
                self.speak_text(f"The clothing type for this event is {event_type}")
                return event_type
        
        print("Unknown Event")
        self.speak_text("Unknown Event")
        return None