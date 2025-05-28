import pickle
import cv2
import mediapipe as mp
import numpy as np
from tkinter import *
import tkinter as tk
import threading
import time
import pyttsx3
from PIL import Image, ImageTk

class SignLanguageDetector:
    def __init__(self):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        
        # Load the trained model
        self.model_dict = pickle.load(open('./model.p', 'rb'))
        self.model = self.model_dict['model']
        
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize detectors with optimized settings
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.3,
            min_tracking_confidence=0.3,
            model_complexity=0
        )
        
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=False,
            min_detection_confidence=0.3,
            min_tracking_confidence=0.3
        )
        
        # Initialize variables
        self.current_letter = ""
        self.formed_text = ""
        self.blink_counter = 0
        self.blink_threshold = 1
        self.last_blink_time = time.time()
        self.blink_cooldown = 1.5
        self.letter_stable_time = 0
        self.letter_stable_threshold = 1.5
        self.last_stable_letter = ""
        self.two_hands_detected = False
        self.two_hands_stable_time = 0
        self.two_hands_threshold = 0.5
        self.last_space_time = 0
        self.space_cooldown = 1.0
        self.frame_count = 0
        self.process_every_n_frames = 2
        
        # Performance monitoring
        self.fps_start_time = time.time()
        self.fps_counter = 0
        self.fps = 0
        
        # Eye indices
        self.LEFT_EYE = [362, 385, 373]
        self.RIGHT_EYE = [33, 160, 133]
        
        # Create GUI
        self.setup_gui()
    
    def setup_gui(self):
        # Set up the main window
        self.root = tk.Tk()
        self.root.title("Sign Language Detection System")
        self.root.configure(bg='#2C3E50')  # Dark blue background
        
        # Make window full screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Left panel (Camera Feed)
        self.left_panel = tk.Frame(self.root, bg='#34495E')  # Slightly lighter blue
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Camera title
        tk.Label(self.left_panel, 
                text="Camera Feed", 
                font=('Helvetica', 24, 'bold'),
                bg='#34495E',
                fg='white').pack(pady=10)
        
        # Camera canvas
        self.camera_frame = tk.Frame(self.left_panel, bg='#2C3E50')
        self.camera_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.camera_canvas = tk.Canvas(self.camera_frame, 
                                     bg='black',
                                     highlightthickness=2,
                                     highlightbackground='#3498DB')  # Blue border
        self.camera_canvas.pack(expand=True, fill='both')
        
        # Current letter display
        self.letter_frame = tk.Frame(self.left_panel, bg='#34495E')
        self.letter_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(self.letter_frame,
                text="Current Letter:",
                font=('Helvetica', 18),
                bg='#34495E',
                fg='white').pack(side='left', padx=10)
        
        self.letter_display = tk.Label(self.letter_frame,
                                     text="",
                                     font=('Helvetica', 36, 'bold'),
                                     bg='#34495E',
                                     fg='#2ECC71')  # Green text
        self.letter_display.pack(side='left', padx=10)
        
        # FPS display
        self.fps_label = tk.Label(self.left_panel,
                                text="FPS: 0",
                                font=('Helvetica', 12),
                                bg='#34495E',
                                fg='#95A5A6')  # Gray text
        self.fps_label.pack(pady=5)
        
        # Right panel (Text and Controls)
        self.right_panel = tk.Frame(self.root, bg='#34495E')
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Text area title
        tk.Label(self.right_panel,
                text="Formed Text",
                font=('Helvetica', 24, 'bold'),
                bg='#34495E',
                fg='white').pack(pady=10)
        
        # Text display
        self.text_frame = tk.Frame(self.right_panel, bg='#2C3E50')
        self.text_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.text_display = tk.Text(self.text_frame,
                                  font=('Helvetica', 16),
                                  wrap='word',
                                  bg='#ECF0F1',  # Light background
                                  fg='#2C3E50',  # Dark text
                                  height=10)
        self.text_display.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Control buttons frame
        self.control_frame = tk.Frame(self.right_panel, bg='#34495E')
        self.control_frame.pack(fill='x', pady=20)
        
        # Modern style buttons
        button_style = {
            'font': ('Helvetica', 12),
            'bg': '#3498DB',  # Blue
            'fg': 'white',
            'activebackground': '#2980B9',  # Darker blue
            'activeforeground': 'white',
            'relief': 'flat',
            'padx': 20,
            'pady': 10
        }
        
        self.clear_button = tk.Button(self.control_frame,
                                    text="Clear Text",
                                    command=self.clear_text,
                                    **button_style)
        self.clear_button.pack(side='left', padx=10)
        
        self.speak_button = tk.Button(self.control_frame,
                                    text="Speak Text",
                                    command=self.speak_text,
                                    **button_style)
        self.speak_button.pack(side='left', padx=10)
        
        self.quit_button = tk.Button(self.control_frame,
                                   text="Quit",
                                   command=self.quit_application,
                                   bg='#E74C3C',  # Red
                                   activebackground='#C0392B',  # Darker red
                                   **{k:v for k,v in button_style.items() if k != 'bg'})
        self.quit_button.pack(side='right', padx=10)
        
        # Instructions
        self.instructions_frame = tk.Frame(self.right_panel, bg='#34495E')
        self.instructions_frame.pack(fill='x', pady=20, padx=20)
        
        tk.Label(self.instructions_frame,
                text="Instructions",
                font=('Helvetica', 18, 'bold'),
                bg='#34495E',
                fg='white').pack(pady=(0,10))
        
        instructions_text = """
• Show hand signs clearly in the camera
• Hold still for 1.5 seconds until letter is confirmed
• Blink to add the letter to text
• Show both hands and hold for space
• Use buttons below to clear or speak text
        """
        
        tk.Label(self.instructions_frame,
                text=instructions_text,
                font=('Helvetica', 12),
                bg='#34495E',
                fg='#BDC3C7',  # Light gray
                justify='left').pack()
        
        # Status bar
        self.status_bar = tk.Frame(self.root, bg='#2C3E50', height=30)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky='ew')
        
        self.status_label = tk.Label(self.status_bar,
                                   text="System Ready",
                                   font=('Helvetica', 10),
                                   bg='#2C3E50',
                                   fg='#95A5A6')
        self.status_label.pack(side='left', padx=10)
    
    def clear_text(self):
        self.formed_text = ""
        self.text_display.delete('1.0', 'end')
        self.status_label.config(text="Text cleared")
    
    def speak_text(self):
        if self.formed_text.strip():
            self.status_label.config(text="Speaking text...")
            self.engine.say(self.formed_text)
            self.engine.runAndWait()
            self.status_label.config(text="Finished speaking")
        else:
            self.status_label.config(text="No text to speak")
    
    def quit_application(self):
        self.root.quit()
    
    def update_gui(self):
        try:
            self.fps_label.config(text=f"FPS: {self.fps:.1f}")
            self.letter_display.config(text=self.current_letter)
            self.text_display.delete('1.0', 'end')
            self.text_display.insert('1.0', self.formed_text)
            self.root.update_idletasks()
        except Exception as e:
            print(f"GUI update error: {e}")
    
    def detect_blink(self, face_landmarks):
        if not face_landmarks:
            return False
        
        # Ultra simplified blink detection
        left_eye_height = abs(face_landmarks[self.LEFT_EYE[0]].y - face_landmarks[self.LEFT_EYE[1]].y)
        return left_eye_height < 0.02  # Only check left eye for speed
    
    def process_frame(self, frame):
        """Process a single frame and return the processed frame"""
        if frame is None:
            return None
            
        frame = cv2.flip(frame, 1)
        H, W, _ = frame.shape
        
        # Create a copy for processing at lower resolution
        process_frame = cv2.resize(frame, (320, 240))
        frame_rgb = cv2.cvtColor(process_frame, cv2.COLOR_BGR2RGB)
        
        # Process hands
        hands_results = self.hands.process(frame_rgb)
        
        # Process face if needed
        face_results = None
        if self.current_letter:
            face_results = self.face_mesh.process(frame_rgb)
        
        current_time = time.time()
        
        # Handle hand detection
        if hands_results.multi_hand_landmarks:
            num_hands = len(hands_results.multi_hand_landmarks)
            
            # Improved two-hand detection for spaces
            if num_hands == 2:
                # Draw both hands for visual feedback
                for hand_landmarks in hands_results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style()
                    )
                
                # Handle two-hand stability for space
                if not self.two_hands_detected:
                    self.two_hands_detected = True
                    self.two_hands_stable_time = current_time
                elif (current_time - self.two_hands_stable_time >= self.two_hands_threshold and 
                      current_time - self.last_space_time >= self.space_cooldown):
                    self.formed_text += " "
                    self.last_space_time = current_time
                    self.status_label.config(text="Space added")
                    self.update_gui()
                
                # Visual feedback for two-hand detection
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
                hand_landmarks = hands_results.multi_hand_landmarks[0]
                
                # Draw landmarks smoothly
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # Process hand data
                data_aux = []
                x_ = []
                y_ = []
                
                for landmark in hand_landmarks.landmark:
                    x_.append(landmark.x)
                    y_.append(landmark.y)
                
                min_x, min_y = min(x_), min(y_)
                
                for landmark in hand_landmarks.landmark:
                    data_aux.extend([landmark.x - min_x, landmark.y - min_y])
                
                # Predict letter
                prediction = self.model.predict([np.asarray(data_aux)])
                predicted_character = prediction[0]
                
                # Draw prediction box and text
                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10
                x2 = int(max(x_) * W) - 10
                y2 = int(max(y_) * H) - 10
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Handle letter stability with visual feedback
                if predicted_character == self.last_stable_letter:
                    if self.letter_stable_time == 0:
                        self.letter_stable_time = current_time
                    
                    # Add progress bar for letter stability
                    progress = min(1.0, (current_time - self.letter_stable_time) / self.letter_stable_threshold)
                    if progress < 1.0:
                        bar_width = int(100 * progress)
                        cv2.rectangle(frame, (x1, y1-30), (x1+100, y1-20), (0, 0, 255), 2)
                        cv2.rectangle(frame, (x1, y1-30), (x1+bar_width, y1-20), (0, 255, 0), -1)
                    
                    if current_time - self.letter_stable_time >= self.letter_stable_threshold:
                        self.current_letter = predicted_character
                        self.update_gui()
                else:
                    self.last_stable_letter = predicted_character
                    self.letter_stable_time = 0
                
                color = (0, 255, 0) if self.letter_stable_time > 0 else (0, 165, 255)
                cv2.putText(frame, predicted_character, (x1, y1 - 40),
                          cv2.FONT_HERSHEY_SIMPLEX, 1.3, color, 3, cv2.LINE_AA)
        
        # Process blinks
        if face_results and face_results.multi_face_landmarks and self.current_letter:
            face_landmarks = face_results.multi_face_landmarks[0].landmark
            if self.detect_blink(face_landmarks):
                if current_time - self.last_blink_time >= self.blink_cooldown:
                    self.formed_text += self.current_letter
                    self.current_letter = ""
                    self.last_blink_time = current_time
                    self.letter_stable_time = 0
                    self.last_stable_letter = ""
                    self.update_gui()
        
        # Add FPS and text overlay
        cv2.putText(frame, f"FPS: {self.fps:.1f}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, f"Text: {self.formed_text}", (10, H-30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
        
        return frame

    def run(self):
        cap = cv2.VideoCapture(0)
        
        # Set optimal camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffer delay
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # FPS calculation
            self.fps_counter += 1
            if time.time() - self.fps_start_time >= 1:
                self.fps = self.fps_counter
                self.fps_counter = 0
                self.fps_start_time = time.time()
            
            # Process frame
            if self.frame_count % self.process_every_n_frames == 0:
                processed_frame = self.process_frame(frame)
                if processed_frame is not None:
                    self.last_processed_frame = processed_frame
            else:
                # Use the last processed frame for smooth display
                processed_frame = self.last_processed_frame if self.last_processed_frame is not None else frame
            
            self.frame_count += 1
            
            # Show the frame
            if processed_frame is not None:
                cv2.imshow('Sign Language Detection', processed_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()

    def start(self):
        camera_thread = threading.Thread(target=self.run)
        camera_thread.daemon = True
        camera_thread.start()
        self.root.mainloop()

if __name__ == "__main__":
    detector = SignLanguageDetector()
    detector.start() 