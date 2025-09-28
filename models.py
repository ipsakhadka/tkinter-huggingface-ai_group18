import os
from transformers import pipeline

# # Disable Hugging Face symlink warning on Windows
# os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

class AIModels:
    def __init__(self):
        # Load Hugging Face models for text_summarization
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        
        #loading image classification model
        self.image_classifier = pipeline("image-classification", model="google/vit-base-patch16-224")
        # google/vit-base-patch16-224 is a pre-trained Vision Transformer for general image recognition

        # this is "encapsulation" GUI just calls the method run_image_classification without needing to know the model detail

      #methods to run the classifications:  
      #method is basically a function that belongs to a class. Here this function belongs to the class AIModels, hence method
    def run_summarization(self, text: str) -> str:
        summary = self.summarizer(text, max_length=60, min_length=15, do_sample=False)
        return summary[0]['summary_text']

    def run_sentiment(self, text: str) -> str:
        sentiment = self.sentiment_analyzer(text)[0]
        return f"{sentiment['label']} (Confidence: {sentiment['score']:.2f})"
    
    def run_image_classification(self, image_path: str) -> str:
       """ takes path of an image and runs classification, then returns the top prediction with 
       confidence score. Eg: if  we upload a pic of a dog, it will display:
       Top Predictions:
       1. labrador (confidence: 0.90) ... likewise
       """

       results = self.image_classifier(image_path) # runs image and returns a list of labels and scores
       output = "Top Predictions:\n"

       for i, r in enumerate (results, start=1):
           label = r['label']
           score = r['score']
           output += f"{i} {label} (Confidence: {score:.2f})\n"
           
       return output #return after the loop
    

    
# Testing methods
""" if __name__ == "__main__": 
    models = AIModels()

    # --- Test Summarization ---
    text = "Tesing if this is functioning as it should, though manually. This is initial phase so shouldn't be a problem. Is manual test that bad? I guess, we'll figure as we go. Let's see!"
    print("---- Summarization Test ----")
    print(models.run_summarization(text))
    
    # --- Test Sentiment Analysis ---
    print("\n---- Sentiment Test ----")
    print(models.run_sentiment(text))

    # --- Test Image Classification ---
    print("\n---- Image Classification Test ----")
    image_path = "cat.jpg"  
    print(models.run_image_classification(image_path))

    """
# output of the above test for reference only:
"""
---- Summarization Test ----
This is initial phase so shouldn't be a problem. Is manual test that bad? I guess, we'll figure as we go. Let's see!

---- Sentiment Test ----
NEGATIVE (Confidence: 0.91)

---- Image Classification Test ----
Top Predictions:
1 tabby, tabby cat (Confidence: 0.85)
2 tiger cat (Confidence: 0.09)
3 Egyptian cat (Confidence: 0.05)
4 Persian cat (Confidence: 0.01)
5 lynx, catamount (Confidence: 0.00)

"""