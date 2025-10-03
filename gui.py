import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import filedialog, messagebox
from models import AIModels
import functools

#Decorator

def log_model_run(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Running model: {func.__name__}")  # Logging model run
        return func(*args, **kwargs)
    return wrapper

# This is our main GUI class. It makes the window and connects everything.
class AIApp(tk.Tk):
    def __init__(self):
        # Call the Tkinter parent class (inheritance!)
        super().__init__()

        # Window settings
        self.title("HIT137 Assignment 3 : Tkinter AI Models GUI")
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
        self.run_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.run_tab, text="Run Models")

        # Input Type Selection 
        input_type_label = tk.Label(self.run_tab, text="Choose input type:", font=("Arial", 12))
        input_type_label.pack(pady=5)

        self.input_type_var = tk.StringVar(value="Text")
        self.input_type_dropdown = ttk.Combobox(
            self.run_tab,
            textvariable=self.input_type_var,
            state="readonly",
            values=["Text", "Image"]
        )
        self.input_type_dropdown.pack(pady=5)


        # Model Selection 
        model_label = tk.Label(self.run_tab, text="Choose a model:", font=("Arial", 12))
        model_label.pack(pady=5)

        self.model_var = tk.StringVar(value="Summarization") 
        self.model_dropdown = ttk.Combobox(
            self.run_tab,
            textvariable=self.model_var,
            state="readonly",
            values=["Summarization", "Sentiment Analysis", "Image Classification"]
        )
        self.model_dropdown.pack(pady=5)

        # Confirm Button + Refresh button 
        #adding the buttons side by side since the stack isn't looking good

        button_frame = tk.Frame(self.run_tab)
        button_frame.pack(pady=10)  # space above/below buttons 
        
        self.confirm_button = tk.Button(
            button_frame, text="Submit", font=("Arial", 12, "bold"),
            bg="white", fg="blue", command=self.confirm_selection
        )

        self.confirm_button.pack(side="left", padx=5, pady=0)

         # ==== Refresh Button ====
        self.refresh_button = tk.Button(
            button_frame, text="Refresh", font=("Arial", 12, "bold"),
            bg="white", fg="green", command=self.refresh_selection
        )
        self.refresh_button.pack(side="left", padx=5, pady=0)

        # Frame for input/output widgets
        self.io_frame = tk.Frame(self.run_tab)
        self.io_frame.pack(fill="both", expand=True, pady=10)

    # ======================
    # CONFIRM SELECTION (between text and image)
    # ======================

    def confirm_selection(self):

        #  Clear previous input/output but keep dropdowns and submit button
        for widget in self.io_frame.winfo_children():
            widget.destroy()
        
        input_type = self.input_type_var.get()
        model_type = self.model_var.get()


        # Check invalid combinations
        if input_type == "Text" and model_type == "Image Classification":
            tk.Label(self.io_frame, text="Invalid selection: Text + Image Classification", fg="red").pack()
            return
        if input_type == "Image" and model_type == "Sentiment Analysis":
            tk.Label(self.io_frame, text="Invalid selection: Image + " + model_type, fg="red").pack()
            return

        # Text + Summarization or Sentiment
        if input_type == "Text":
            tk.Label(self.io_frame, text="Enter your text:", font=("Arial", 12)).pack(pady=5)
            self.text_input = tk.Text(self.io_frame, height=6, width=70)
            self.text_input.pack(pady=5)

            tk.Button(
                self.io_frame, text="Submit", font=("Arial", 12, "bold"),
                bg="white", fg="green",
                command=lambda: self.run_text_model(model_type)
            ).pack(pady=10)

            tk.Label(self.io_frame, text="Model Output:", font=("Arial", 12, "bold")).pack(pady=5)
            self.output_text = tk.Text(self.io_frame, height=6, width=60, state="disabled")
            self.output_text.pack(pady=5)
            return

    # Image + Image Classification or Summarization

        elif input_type == "Image":
            tk.Button(
                self.io_frame, text="Upload Image", font=("Arial", 12, "bold"),
                bg="white", fg="blue", command=self.upload_image
            ).pack(pady=5)

            tk.Button(
                self.io_frame, text="Submit", font=("Arial", 12, "bold"),
                    bg="white", fg="green",
                command=lambda: self.run_image_model(model_type)
            ).pack(pady=10)

            tk.Label(self.io_frame, text="Model Output:", font=("Arial", 12, "bold")).pack(pady=5)
            self.output_text = tk.Text(self.io_frame, height=6, width=60, state="disabled")
            self.output_text.pack(pady=5)
            return



        
## this shows confirm button and is functional, but when double clicked it shows multiple times, 
## required update here would be: to fix the button (right now, it's transparent and need to be clicked see the text)
## also, should click only once and then perform action or refresh. 


    @log_model_run #decorator added    
    def run_text_model(self, selected_model):
        text = self.text_input.get("1.0", tk.END).strip()
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)

        if not text:
            self.output_text.insert(tk.END, "Please enter some text first!")
            self.output_text.config(state="disabled")
            return

        try:
            if selected_model == "Summarization":
                result = self.models.run_summarization(text)
                self.output_text.insert(tk.END, "Summary:\n" + result)
            elif selected_model == "Sentiment Analysis":
                result = self.models.run_sentiment(text)
                self.output_text.insert(tk.END, "Sentiment: " + result)
        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}")
        finally:
            self.output_text.config(state="disabled")


    def run_image_model(self, selected_model):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)

        if not hasattr(self, "image_path") or not self.image_path:
            self.output_text.insert(tk.END, "Please upload an image first!")
            self.output_text.config(state="disabled")
            return

        try:
            if selected_model == "Image Classification":
                result = self.models.run_image_classification(self.image_path)
                self.output_text.insert(tk.END, result)
            elif selected_model == "Summarization":
                extracted_text = self.models.run_ocr(self.image_path)
                result = self.models.run_summarization(extracted_text)
                self.output_text.insert(tk.END, "Summary:\n" + result)
        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}")
        finally:
            self.output_text.config(state="disabled")


    @log_model_run
    def upload_image(self):
        self.image_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        if not self.image_path:
            self.output_text.insert(tk.END, "No image selected!")
        else:
            self.output_text.insert(tk.END, f"Image selected: {self.image_path}")
        self.output_text.config(state="disabled")



       

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

3) Image Classification Model: google/vit-base-patch16-224
   - Type: Vision Transformer (ViT)
   - Task: Classifies images into categories (e.g., animals, objects)
   - Strength: General-purpose, can recognize a wide range of images
   - Weakness: Might misclassify uncommon objects or very small details
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
            text = self.text_input.get("1.0", tk.END).strip()
            if not text:
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, "Please enter some text first!")
                return
        #adding the image input type
        elif input_type == "Image":
            image_path = filedialog.askopenfilename(
                title = "Select an image",
                filetypes = [("Image files", "*.jpg *.jpeg *.png *bmp *.gif")]
            )
            if not image_path:
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, "No image selected!")
                return   
            # Run the image classifier
            result = self.models.run_image_classification(image_path)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, result)
            return  # exit function after running image classifier     
        
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

    def refresh_selection(self):
        """Reset the Run tab to allow new selections"""
        # Clear input/output frame
        for widget in self.io_frame.winfo_children():
            widget.destroy()

        # Reset dropdowns back to defaults
        self.input_type_var.set("Text")  # clear input type
        self.model_var.set("Summarization")  # clear model selection


if __name__ == "__main__":
    app = AIApp()   # create the GUI object
    app.mainloop()  # start the event loop
