import pickle
import cv2
import mediapipe as mp
import numpy as np
import time
import customtkinter as ctk
import threading
import pyttsx3
from PIL import Image, ImageTk
from deep_translator import GoogleTranslator
from textblob import Word
import json

class SignLanguageDetector:
    def __init__(self):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        
        # Initialize MediaPipe and model
        self.model_dict = pickle.load(open('./model.p', 'rb'))
        self.model = self.model_dict['model']
        
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize hands detection
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.3,
            min_tracking_confidence=0.3
        )
        
        # Timing and stability settings
        self.letter_stable_time = 0
        self.letter_stable_threshold = 1.5
        self.last_stable_letter = ""
        self.current_letter = ""
        self.formed_text = ""
        
        # Two-hand space settings
        self.two_hands_detected = False
        self.two_hands_stable_time = 0
        self.two_hands_threshold = 0.5
        self.last_space_time = 0
        self.space_cooldown = 1.0
        
        # Translation settings
        self.languages = {
            'English': 'en',
            'Telugu': 'te',
            'Hindi': 'hi',
            'Tamil': 'ta',
            'German': 'de'
        }
        self.current_language = 'English'
        self.translated_text = ""
        
        # Word suggestions
        self.suggestions = []
        self.last_word = ""
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create GUI
        self.setup_gui()
        
    def setup_gui(self):
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Sign Language Text Display")
        self.root.geometry("1600x900")  # Increased window size
        
        # Create main container
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Split into left and right frames
        # Left frame for camera
        left_frame = ctk.CTkFrame(main_container)
        left_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        # Right frame for text and controls
        right_frame = ctk.CTkFrame(main_container)
        right_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # Camera label (placeholder for camera feed)
        self.camera_label = ctk.CTkLabel(left_frame)
        self.camera_label.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Right side content
        # Current Letter Display
        self.letter_display = ctk.CTkLabel(
            right_frame,
            text="Current Letter: ",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        self.letter_display.pack(pady=10)
        
        # Text display
        text_frame = ctk.CTkFrame(right_frame)
        text_frame.pack(fill="both", expand=True, pady=10)
        
        # Original text display
        self.text_display = ctk.CTkTextbox(
            text_frame,
            font=ctk.CTkFont(size=16),
            wrap="word",
            height=150
        )
        self.text_display.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Word suggestions frame
        suggestions_frame = ctk.CTkFrame(text_frame)
        suggestions_frame.pack(fill="x", padx=10, pady=5)
        
        self.suggestion_buttons = []
        for i in range(5):
            btn = ctk.CTkButton(
                suggestions_frame,
                text="",
                width=120,
                height=30,
                command=lambda x=i: self.use_suggestion(x)
            )
            btn.pack(side="left", padx=2)
            self.suggestion_buttons.append(btn)
        
        # Translation frame
        translation_frame = ctk.CTkFrame(text_frame)
        translation_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Language selection
        language_frame = ctk.CTkFrame(translation_frame)
        language_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            language_frame,
            text="Translation Language:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=5)
        
        self.language_var = ctk.StringVar(value="English")
        language_menu = ctk.CTkOptionMenu(
            language_frame,
            values=list(self.languages.keys()),
            variable=self.language_var,
            command=self.change_language
        )
        language_menu.pack(side="left", padx=5)
        
        # Translated text display
        self.translation_display = ctk.CTkTextbox(
            translation_frame,
            font=ctk.CTkFont(size=16),
            wrap="word",
            height=150
        )
        self.translation_display.pack(fill="both", expand=True, pady=5)
        
        # Controls frame
        controls_frame = ctk.CTkFrame(right_frame)
        controls_frame.pack(fill="x", pady=10)
        
        # Button style configuration
        button_width = 120
        button_height = 35
        
        # Clear button
        self.clear_btn = ctk.CTkButton(
            controls_frame,
            text="Clear Text",
            width=button_width,
            height=button_height,
            command=self.clear_text,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.clear_btn.pack(side="left", padx=5)
        
        # Speak Original button
        self.speak_btn = ctk.CTkButton(
            controls_frame,
            text="Speak Original",
            width=button_width,
            height=button_height,
            command=lambda: self.speak_text(False),
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.speak_btn.pack(side="left", padx=5)
        
        # Speak Translated button
        self.speak_translated_btn = ctk.CTkButton(
            controls_frame,
            text="Speak Translated",
            width=button_width,
            height=button_height,
            command=lambda: self.speak_text(True),
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.speak_translated_btn.pack(side="left", padx=5)
        
        # Status bar
        self.status_bar = ctk.CTkLabel(
            right_frame,
            text="System Ready",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.status_bar.pack(pady=5)
        
    def setup_instructions(self, container):
        instructions_frame = ctk.CTkFrame(container)
        instructions_frame.pack(fill="x", pady=10)
        
        instructions_title = ctk.CTkLabel(
            instructions_frame,
            text="Instructions",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        instructions_title.pack(pady=5)
        
        instructions_text = """
• Show hand signs clearly in the camera
• Hold still for 1.5 seconds to confirm a letter
• Show both hands for space
• Select language for translation
• Click on word suggestions to use them
• Use speak buttons for audio in either language
        """
        
        instructions = ctk.CTkLabel(
            instructions_frame,
            text=instructions_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        instructions.pack(pady=5)
    
    def use_suggestion(self, index):
        if index < len(self.suggestions):
            # Replace the last word with the suggestion
            words = self.formed_text.split()
            if words:
                words[-1] = self.suggestions[index]
                self.formed_text = " ".join(words)
                self.update_text_display()
    
    def update_suggestions(self):
        words = self.formed_text.split()
        if words:
            current_word = words[-1]
            if current_word != self.last_word:
                self.last_word = current_word
                try:
                    word = Word(current_word)
                    # Get suggestions (similar words and corrections)
                    self.suggestions = word.suggest()[:5]
                    # Update suggestion buttons
                    for i, btn in enumerate(self.suggestion_buttons):
                        if i < len(self.suggestions):
                            btn.configure(text=self.suggestions[i])
                        else:
                            btn.configure(text="")
                except:
                    self.suggestions = []
                    for btn in self.suggestion_buttons:
                        btn.configure(text="")
    
    def change_language(self, language):
        self.current_language = language
        self.translate_text()
    
    def translate_text(self):
        if self.formed_text.strip():
            try:
                translator = GoogleTranslator(
                    source='en',
                    target=self.languages[self.current_language]
                )
                self.translated_text = translator.translate(self.formed_text)
                self.translation_display.delete('1.0', "end")
                self.translation_display.insert('1.0', self.translated_text)
            except Exception as e:
                self.status_bar.configure(text=f"Translation error: {str(e)}")
        else:
            self.translation_display.delete('1.0', "end")
    
    def clear_text(self):
        self.formed_text = ""
        self.translated_text = ""
        self.text_display.delete('1.0', "end")
        self.translation_display.delete('1.0', "end")
        self.status_bar.configure(text="Text cleared")
        
    def speak_text(self, translated=False):
        text = self.translated_text if translated else self.formed_text
        if text:
            self.status_bar.configure(text="Speaking text...")
            self.engine.say(text)
            self.engine.runAndWait()
            self.status_bar.configure(text="Finished speaking")
        else:
            self.status_bar.configure(text="No text to speak")
            
    def update_text_display(self):
        self.text_display.delete('1.0', "end")
        self.text_display.insert('1.0', self.formed_text)
        self.update_suggestions()
        self.translate_text()
        self.root.update()
        
    def process_frame(self, frame):
        H, W, _ = frame.shape
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = self.hands.process(frame_rgb)
        current_time = time.time()
        
        if results.multi_hand_landmarks:
            num_hands = len(results.multi_hand_landmarks)
            
            if num_hands == 2:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style()
                    )
                
                if not self.two_hands_detected:
                    self.two_hands_detected = True
                    self.two_hands_stable_time = current_time
                elif (current_time - self.two_hands_stable_time >= self.two_hands_threshold and 
                      current_time - self.last_space_time >= self.space_cooldown):
                    self.formed_text += " "
                    self.last_space_time = current_time
                    self.update_text_display()
                    
                progress = min(1.0, (current_time - self.two_hands_stable_time) / self.two_hands_threshold)
                if progress < 1.0:
                    bar_width = int(200 * progress)
                    cv2.rectangle(frame, (W//2-100, 50), (W//2+100, 70), (0, 0, 255), 2)
                    cv2.rectangle(frame, (W//2-100, 50), (W//2-100+bar_width, 70), (0, 255, 0), -1)
                    cv2.putText(frame, "Hold for space", (W//2-100, 45),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
            
            else:
                self.two_hands_detected = False
                self.two_hands_stable_time = 0
                
                hand_landmarks = results.multi_hand_landmarks[0]
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
                
                data_aux = []
                x_ = []
                y_ = []
                
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    x_.append(x)
                    y_.append(y)
                
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))
                
                prediction = self.model.predict([np.asarray(data_aux)])
                predicted_character = prediction[0]
                
                if predicted_character == self.last_stable_letter:
                    if self.letter_stable_time == 0:
                        self.letter_stable_time = current_time
                    
                    progress = min(1.0, (current_time - self.letter_stable_time) / self.letter_stable_threshold)
                    bar_width = int(100 * progress)
                    
                    x1 = int(min(x_) * W) - 10
                    y1 = int(min(y_) * H) - 10
                    x2 = int(max(x_) * W) - 10
                    y2 = int(max(y_) * H) - 10
                    
                    cv2.rectangle(frame, (x1, y1-30), (x1+100, y1-20), (0, 0, 255), 2)
                    cv2.rectangle(frame, (x1, y1-30), (x1+bar_width, y1-20), (0, 255, 0), -1)
                    
                    if current_time - self.letter_stable_time >= self.letter_stable_threshold:
                        self.formed_text += predicted_character
                        self.letter_stable_time = 0
                        self.update_text_display()
                        
                    color = (0, 255, 0)
                    self.letter_display.configure(text=f"Current Letter: {predicted_character}")
                else:
                    self.last_stable_letter = predicted_character
                    self.letter_stable_time = 0
                    color = (0, 165, 255)
                    self.letter_display.configure(text=f"Current Letter: {predicted_character}")
                
                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10
                x2 = int(max(x_) * W) - 10
                y2 = int(max(y_) * H) - 10
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, predicted_character, (x1, y1 - 40),
                          cv2.FONT_HERSHEY_SIMPLEX, 1.3, color, 3, cv2.LINE_AA)
        
        cv2.putText(frame, "Show two hands for space", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
        
        return frame
    
    def update_camera_feed(self, frame):
        # Convert OpenCV BGR frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to PhotoImage
        image = Image.fromarray(frame_rgb)
        photo = ImageTk.PhotoImage(image=image)
        
        # Update camera label
        self.camera_label.configure(image=photo)
        self.camera_label.image = photo  # Keep a reference!
        
        # Update the GUI
        self.root.update()

    def run_camera(self):
        cap = cv2.VideoCapture(0)
        
        # Set camera resolution to match the frame
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            processed_frame = self.process_frame(frame)
            self.update_camera_feed(processed_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
        self.root.quit()
    
    def start(self):
        # Start camera thread
        camera_thread = threading.Thread(target=self.run_camera)
        camera_thread.daemon = True
        camera_thread.start()
        
        # Start GUI
        self.root.mainloop()

if __name__ == "__main__":
    detector = SignLanguageDetector()
    detector.start()
