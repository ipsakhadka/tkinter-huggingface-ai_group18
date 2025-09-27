import tkinter as tk
from tkinter import ttk, scrolledtext
from models import AIModels

# This is our main GUI class. It makes the window and connects everything.
class AIApp(tk.Tk):
    def __init__(self):
        # Call the Tkinter parent class (inheritance!)
        super().__init__()

        # Window settings
        self.title("HIT137 Assignment 3 - Tkinter AI Models GUI")
        self.geometry("800x600")
        self.configure(bg="#f4f4f4")

        # Load Hugging Face models (from models.py)
        self.models = AIModels()

        # Create tabs like in the sample GUI
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Making 3 tabs
        self.create_run_tab()
        self.create_model_info_tab()
        self.create_explanation_tab()

    # ======================
    # TAB 1: Run Models
    # ======================
    def create_run_tab(self):
        # Frame for tab
        run_frame = ttk.Frame(self.notebook)
        self.notebook.add(run_frame, text="Run Models")

        # Input Type Selection 
        input_type_label = tk.Label(run_frame, text="Select Input Type:", font=("Arial", 12))
        input_type_label.pack(pady=5)
        self.input_type_var = tk.StringVar(value="Text")  # (default)
        self.input_type_dropdown = ttk.Combobox(
            run_frame,
            textvariable=self.input_type_var,
            state="readonly",
            values=["Text", "Image", "Audio"]  # (only text works now)
        )
        self.input_type_dropdown.pack(pady=5)

        # Model Selection 
        model_label = tk.Label(run_frame, text="Choose a model:", font=("Arial", 12))
        model_label.pack(pady=5)
        self.model_var = tk.StringVar(value="Summarization")  # (default)
        self.model_dropdown = ttk.Combobox(
            run_frame,
            textvariable=self.model_var,
            state="readonly",
            values=["Summarization", "Sentiment Analysis"]
        )
        self.model_dropdown.pack(pady=5)

        # Input Text Area (for text input only) 
        input_label = tk.Label(run_frame, text="Enter your text:", font=("Arial", 12))
        input_label.pack(pady=5)
        self.input_text = scrolledtext.ScrolledText(
            run_frame, wrap=tk.WORD, width=90, height=8, font=("Arial", 11)
        )
        self.input_text.pack(pady=5)

        # Run Button 
        run_button = tk.Button(
            run_frame, text="Run Model", font=("Arial", 12, "bold"),
            command=self.run_model, bg="#007acc", fg="white", relief="raised"
        )
        run_button.pack(pady=10)

        # Output Area 
        output_label = tk.Label(run_frame, text="Model Output:", font=("Arial", 12))
        output_label.pack(pady=5)
        self.output_text = scrolledtext.ScrolledText(
            run_frame, wrap=tk.WORD, width=90, height=10, font=("Arial", 11)
        )
        self.output_text.pack(pady=5)

    # ======================
    # TAB 2: Model Information
    # ======================
    def create_model_info_tab(self):
        # Frame for tab
        info_frame = ttk.Frame(self.notebook)
        self.notebook.add(info_frame, text="Model Information")

        # Text box (read-only)
        info_text = scrolledtext.ScrolledText(info_frame, wrap=tk.WORD, width=90, height=25, font=("Arial", 11))
        info_text.pack(pady=10, padx=10)

        # Info about the models
        model_info = """
Model Information

1) Summarization Model: facebook/bart-large-cnn
   - Type: Sequence-to-sequence transformer
   - Task: Summarizes long text into short text
   - Strength: Great for articles or reports
   - Weakness: Can miss small details if text is too long

2) Sentiment Analysis Model: distilbert-base-uncased-finetuned-sst-2-english
   - Type: DistilBERT (small, fast version of BERT)
   - Task: Checks if text is Positive or Negative
   - Strength: Fast and accurate
   - Weakness: Only knows 2 moods (positive/negative)
"""
        info_text.insert(tk.END, model_info)
        info_text.config(state="disabled")  # lock text

    # ======================
    # TAB 3: Explanations
    # ======================
    def create_explanation_tab(self):
        # Frame for tab
        explain_frame = ttk.Frame(self.notebook)
        self.notebook.add(explain_frame, text="Explanations")

        # Text box (read-only)
        explain_text = scrolledtext.ScrolledText(explain_frame, wrap=tk.WORD, width=90, height=25, font=("Arial", 11))
        explain_text.pack(pady=10, padx=10)

        # Explain OOP like a student
        oop_explanation = """
Explanation of OOP Concepts in This Project

1) Inheritance:
   - Our AIApp class gets features from tkinter.Tk.
   - Means we don’t need to build everything from scratch.

2) Encapsulation:
   - The models are inside AIModels class in models.py.
   - The GUI just uses simple functions, doesn’t touch inside code.

3) Polymorphism:
   - run_model() acts different depending on which model we select.
   - Same function name, different output.

4) Method Overriding:
   - Tkinter has __init__ already.
   - We override it in AIApp to set up our own GUI stuff.

5) Multiple Files:
   - models.py = model code
   - gui.py = GUI code
   - main.py = starts the program
"""
        explain_text.insert(tk.END, oop_explanation)
        explain_text.config(state="disabled")  # lock text

    # ======================
    # RUN MODEL FUNCTION
    # ======================
    def run_model(self):
        # Grab the selected input type
        input_type = self.input_type_var.get()

        # If it's text, we use the text box
        if input_type == "Text":
            text = self.input_text.get("1.0", tk.END).strip()
            if not text:
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, "Please enter some text first!")
                return
        else:
            # Placeholder for Image/Audio (not implemented yet)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"{input_type} input is not supported yet.")
            return

        # Clear previous output
        self.output_text.delete("1.0", tk.END)
        selected_model = self.model_var.get()

        try:
            if selected_model == "Summarization":
                result = self.models.run_summarization(text)
                self.output_text.insert(tk.END, "Summary:\n" + result)

            elif selected_model == "Sentiment Analysis":
                result = self.models.run_sentiment(text)
                self.output_text.insert(tk.END, "Sentiment: " + result)

        except Exception as e:
            self.output_text.insert(tk.END, f"Error running model: {str(e)}")
