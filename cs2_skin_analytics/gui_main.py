# gui_main.py
import sys
import tkinter as tk
from tkinter import font
from src.scraper import run_scraper
from src.data_cleaning import clean_raw_data
from src.models import train_regression_model, train_classifier_model

class RedirectText:
    """Helper class to redirect stdout print statements directly into the Tkinter Text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)  # Auto-scroll to the bottom

    def flush(self):
        pass

def run_pipeline(output_widget, window):
    """Executes the standard pipeline while streaming outputs into the GUI window."""
    # Redirect standard print statements to the GUI text box
    sys.stdout = RedirectText(output_widget)
    
    try:
        print("[1/3] Initializing pipeline extraction layout scripts...")
        raw_data = run_scraper()
        
        print("[2/3] Executing structural cleanup, reshaping, and target generation...")
        X, y_reg, y_clf = clean_raw_data(raw_data)
        
        print("[3/3] Training pipelines and compiling diagnostic loss matrices...")
        train_regression_model(X, y_reg)
        train_classifier_model(X, y_clf)
        
        print("\nPipeline analytics processed flawlessly.")
    except Exception as e:
        print(f"\n[ERROR] Pipeline crashed: {str(e)}")
    finally:
        # Restore normal terminal stdout behavior when done
        sys.stdout = sys.__stdout__

def create_gui():
    # Initialize the main window shell
    root = tk.Tk()
    root.title("CS2 Skin Analytics Pipeline")
    root.geometry("750x650")
    root.configure(bg="#1e1e24")  # Minimalist dark slate canvas
    
    # Define clean, elegant font pairings
    title_font = font.Font(family="Helvetica", size=14, weight="bold")
    mono_font = font.Font(family="Consolas", size=10)
    
    # Window Header Frame
    header_frame = tk.Frame(root, bg="#1e1e24")
    header_frame.pack(fill=tk.X, padx=30, pady=(25, 10))
    
    title_label = tk.Label(
        header_frame, 
        text="MARKET ANALYTICS ENGINE", 
        fg="#ffffff", 
        bg="#1e1e24", 
        font=title_font,
    )
    title_label.pack(side=tk.LEFT)
    
    # Execution Button (Minimalist borderless design)
    run_btn = tk.Button(
        header_frame, 
        text="RUN ANALYSIS", 
        command=lambda: run_pipeline(output_area, root),
        bg="#3a3d52", 
        fg="#ffffff", 
        activebackground="#515570",
        activeforeground="#ffffff",
        bd=0, 
        padx=15, 
        pady=6,
        font=("Helvetica", 9, "bold"),
        cursor="hand2"
    )
    run_btn.pack(side=tk.RIGHT)
    
    # Separate line decoration
    divider = tk.Frame(root, bg="#2d3142", height=1)
    divider.pack(fill=tk.X, padx=30, pady=10)
    
    # Terminal Display Output Area Frame
    display_frame = tk.Frame(root, bg="#1e1e24")
    display_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))
    
    # Pure text matrix display block
    output_area = tk.Text(
        display_frame, 
        bg="#16161a", 
        fg="#cbd5e1", 
        insertbackground="white", 
        bd=0, 
        font=mono_font,
        padx=15, 
        pady=15,
        spacing1=3, # Padding between log lines
        wrap=tk.WORD
    )
    output_area.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
    
    # Clean custom matching scrollbar element
    scrollbar = tk.Scrollbar(display_frame, bd=0, width=8)
    scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
    
    # Link scrollbar functionality to the output window
    output_area.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=output_area.yview)
    
    # Provide initial minimalist user instruction inside the text frame
    output_area.insert(tk.END, "System Idle. Click 'RUN ANALYSIS' above to spin up model training metrics...\n")
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
