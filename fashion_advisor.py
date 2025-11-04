from ultralytics import YOLO
import cv2
import time
import google.generativeai as genai
from dotenv import load_dotenv
import os

class FashionAdvisor:
    def __init__(self):
        load_dotenv()
        
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        
        self.model = YOLO("best.pt")
        
        self.clothing_categories = {
            'blazers': 'business',
            'coats': 'formal',
            'dress': 'formal',
            'shoes': 'variable',
            'hoodies': 'casual',
            'pants': 'variable',
            'shirts': 'variable',
            'shorts': 'casual',
            'sunglasses': 'casual',
            't-shirt': 'casual',
            'football shoes': 'activewear'
        }

    def detect_clothing(self, capture_time=20):
        detected_clothing_set = set()
        cap = cv2.VideoCapture(0)
        start_time = time.time()

        while time.time() - start_time < capture_time:
            ret, frame = cap.read()
            if not ret:
                print("Error: could not read frame from webcam.")
                break

            results = self.model.predict(frame, conf=0.3, save=True, show=True)
            
            for result in results:
                for box in result.boxes:
                    cls = int(box.cls[0])
                    cls_name = self.model.names[cls]
                    detected_clothing_set.add(cls_name.lower())

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return list(detected_clothing_set)

    def get_fashion_advice(self, detected_items, event_description):
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""As a fashion advisor, analyze this outfit for a {event_description} event:
        Detected clothing items: {', '.join(detected_items)}
        
        Please provide:
        1. Whether this outfit is appropriate for the event
        2. If not appropriate, suggest specific improvements
        3. Additional styling tips if needed
        
        Keep the response concise and practical."""
        
        response = model.generate_content(prompt)
        return response.text