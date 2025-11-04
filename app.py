# Main application file that brings together speech recognition and fashion advice
from speech_recognition import SpeechHandler
from fashion_advisor import FashionAdvisor

def main():
    speech_handler = SpeechHandler()
    fashion_advisor = FashionAdvisor()

    text, event_type = speech_handler.get_event_from_speech()
    
    if event_type is None:
        return

    detected_items = fashion_advisor.detect_clothing()
    
    advice = fashion_advisor.get_fashion_advice(detected_items, text)
    
    print("Fashion Advice:", advice)
    speech_handler.speak_text(advice)

if __name__ == "__main__":
    main()