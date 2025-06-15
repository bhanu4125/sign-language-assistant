import pickle
import cv2
import mediapipe as mp
import numpy as np
import time

class SimpleSignDetector:
    def __init__(self):
        # Load model
        try:
            self.model_dict = pickle.load(open('./model.p', 'rb'))
            self.model = self.model_dict['model']
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            exit(1)
        
        # Initialize MediaPipe
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
                    print(f"Current text: {self.formed_text}")
                    
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
                        print(f"Current text: {self.formed_text}")
                        
                    color = (0, 255, 0)
                    self.current_letter = predicted_character
                else:
                    self.last_stable_letter = predicted_character
                    self.letter_stable_time = 0
                    color = (0, 165, 255)
                    self.current_letter = predicted_character
                
                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10
                x2 = int(max(x_) * W) - 10
                y2 = int(max(y_) * H) - 10
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, predicted_character, (x1, y1 - 40),
                          cv2.FONT_HERSHEY_SIMPLEX, 1.3, color, 3, cv2.LINE_AA)
                
                # Show the current letter and text
                cv2.putText(frame, f"Current letter: {self.current_letter}", (10, H - 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, f"Text: {self.formed_text}", (10, H - 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
        
        cv2.putText(frame, "Show two hands for space", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
        
        return frame
    
    def run(self):
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return
        
        # Set camera resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        
        print("Camera opened successfully. Press 'q' to quit.")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture image from camera.")
                break
                
            processed_frame = self.process_frame(frame)
            
            # Display the frame
            cv2.imshow('Sign Language Detection', processed_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
        
        print("Final text:", self.formed_text)

if __name__ == "__main__":
    print("Starting simple sign language detector...")
    print("Press 'q' to quit")
    detector = SimpleSignDetector()
    detector.run() 