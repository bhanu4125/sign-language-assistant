import customtkinter as ctk
from tkinter import messagebox
import subprocess
import os
import webbrowser
import sys
import importlib.util

class SignLanguageAssistant:
    def __init__(self):
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("Sign Language Assistant")
        self.root.geometry("800x500")
        
        # Create header
        title = ctk.CTkLabel(
            self.root,
            text="Sign Language Assistant",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.pack(pady=30)
        
        # Create main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(expand=True, fill="both", padx=40, pady=20)
        
        # Create buttons frame
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(expand=True, pady=20)
        
        # Sign to Text button with description
        sign_frame = ctk.CTkFrame(buttons_frame)
        sign_frame.pack(pady=20, padx=30, fill="x")
        
        ctk.CTkButton(
            sign_frame,
            text="Sign Language to Text",
            command=self.launch_sign_to_text,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50
        ).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            sign_frame,
            text="Launch the sign language detection application",
            font=ctk.CTkFont(size=12)
        ).pack()
        
        # Text to Sign button with description
        text_frame = ctk.CTkFrame(buttons_frame)
        text_frame.pack(pady=20, padx=30, fill="x")
        
        ctk.CTkButton(
            text_frame,
            text="Text to Sign Language",
            command=self.launch_text_to_sign,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50
        ).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            text_frame,
            text="Open the text to sign language converter",
            font=ctk.CTkFont(size=12)
        ).pack()
        
        # Status bar
        self.status_label = ctk.CTkLabel(
            self.root,
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=10)

    def check_dependencies(self):
        try:
            import cv2
            import mediapipe
            import numpy
            import customtkinter
            import pyttsx3
            from PIL import Image
            from deep_translator import GoogleTranslator
            from textblob import Word
            return True
        except ImportError as e:
            return False

    def check_model_file(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, "model.p")
        return os.path.exists(model_path)

    def install_dependencies(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            setup_bat = os.path.join(current_dir, "setup.bat")
            subprocess.run([setup_bat], shell=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            return False

    def launch_sign_to_text(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Check model file first
            if not self.check_model_file():
                messagebox.showerror(
                    "Error",
                    "model.p file not found!\n\nPlease ensure the model file is in the same directory."
                )
                return
            
            # Check dependencies only if model exists
            if not self.check_dependencies():
                response = messagebox.askyesno(
                    "Missing Dependencies",
                    "Some required packages are missing.\nWould you like to install them now?"
                )
                if response:
                    self.status_label.configure(text="Installing dependencies...")
                    if not self.install_dependencies():
                        messagebox.showerror(
                            "Error",
                            "Failed to install dependencies.\nPlease try running setup.bat manually."
                        )
                        return
                else:
                    return
            
            # Try to launch the application
            try:
                self.status_label.configure(text="Launching sign language detection...")
                subprocess.Popen([
                    sys.executable,
                    os.path.join(current_dir, "sign_language_detector_final.py")
                ])
                self.status_label.configure(text="Application launched successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to launch application: {str(e)}")
                self.status_label.configure(text="Failed to launch application")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.configure(text="Error occurred")

    def launch_text_to_sign(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            html_path = os.path.join(current_dir, "text_to_sign.html")
            
            if not os.path.exists(html_path):
                messagebox.showerror(
                    "Error",
                    "text_to_sign.html not found!\n\nPlease ensure the file exists in the application directory."
                )
                return
                
            self.status_label.configure(text="Opening text to sign converter...")
            webbrowser.open(f'file:///{html_path}')
            self.status_label.configure(text="Text to sign converter opened")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch Text to Sign: {str(e)}")
            self.status_label.configure(text="Failed to open text to sign converter")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SignLanguageAssistant()
    app.run() 