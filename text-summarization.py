from transformers import pipeline

# Create a summarization pipeline
model = pipeline(task="summarization", model="facebook/bart-large-cnn")

# Run summarization
response = model("The Hugging Face Transformers library provides thousands of pretrained models to perform tasks on text such as classification, information extraction, question answering, summarization, translation, text generation and more.")
print(response)
