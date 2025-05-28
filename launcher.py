import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import webbrowser
import sys

class SignLanguageAssistant:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sign Language Assistant")
        self.root.geometry("600x400")
        self.root.configure(bg='white')

        # Create header
        title = tk.Label(
            self.root,
            text="Sign Language Assistant",
            font=("Arial", 24, "bold"),
            bg='white'
        )
        title.pack(pady=20)

        # Create buttons frame
        buttons_frame = tk.Frame(self.root, bg='white')
        buttons_frame.pack(expand=True)

        # Sign to Text button
        self.create_button(
            buttons_frame,
            "Sign Language to Text",
            "Launch the sign language detection application",
            self.launch_sign_to_text
        )

        # Text to Sign button
        self.create_button(
            buttons_frame,
            "Text to Sign Language",
            "Open the text to sign language converter",
            self.launch_text_to_sign
        )

    def create_button(self, parent, text, description, command):
        frame = tk.Frame(parent, bg='white', pady=10)
        frame.pack()

        # Main button
        btn = tk.Button(
            frame,
            text=text,
            command=command,
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        btn.pack()

        # Description
        desc = tk.Label(
            frame,
            text=description,
            font=("Arial", 10),
            bg='white',
            fg='gray'
        )
        desc.pack(pady=5)

    def launch_sign_to_text(self):
        try:
            # Change to the correct directory
            os.chdir(r"C:\Users\tumma\OneDrive\Documents\2nd chance\dti 2")
            
            # Run the Python script
            subprocess.Popen([
                r"c:\Users\tumma\Downloads\vs code\python\sign-language-detector-python-master\DTI\.venv\Scripts\python.exe",
                "inference_classifier.py"
            ])
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch Sign to Text: {str(e)}")

    def launch_text_to_sign(self):
        try:
            html_path = r"C:\Users\tumma\OneDrive\Documents\2nd chance\text to sign\index.html"
            webbrowser.open(f'file:///{html_path}')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch Text to Sign: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SignLanguageAssistant()
    app.run() 