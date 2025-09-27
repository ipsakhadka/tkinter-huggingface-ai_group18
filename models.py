import os
from transformers import pipeline

# # Disable Hugging Face symlink warning on Windows
# os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

class AIModels:
    def __init__(self):
        # Load Hugging Face models
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    def run_summarization(self, text: str) -> str:
        summary = self.summarizer(text, max_length=60, min_length=15, do_sample=False)
        return summary[0]['summary_text']

    def run_sentiment(self, text: str) -> str:
        sentiment = self.sentiment_analyzer(text)[0]
        return f"{sentiment['label']} (Confidence: {sentiment['score']:.2f})"
