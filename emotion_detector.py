# emotion_detector.py

from transformers import pipeline

class EmotionDetector:
    def __init__(self):
        self.classifier = pipeline("sentiment-analysis")  # Using default (distilBERT-based)

    def detect(self, text):
        try:
            result = self.classifier(text)[0]
            label = result["label"].lower()
            if label == "positive":
                emotion = "positive"
            elif label == "negative":
                emotion = "negative"
            else:
                emotion = "neutral"
            return {"emotion": emotion, "confidence": round(result["score"], 2)}
        except Exception as e:
            return {"error": str(e)}
