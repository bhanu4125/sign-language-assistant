import pickle
import cv2
import mediapipe as mp
import numpy as np
import time
import os

print("====== Sign Language to Text Detector ======")
print("Loading model and initializing camera...")

try:
    # Load model
    model_path = './model.p'
    if not os.path.exists(model_path):
        print(f"ERROR: Model file not found at {os.path.abspath(model_path)}")
        exit(1)
        
    model_dict = pickle.load(open(model_path, 'rb'))
    model = model_dict['model']
    print("Model loaded successfully")
    
    # Initialize MediaPipe
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    
    # Initialize hands detection
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.3,
        min_tracking_confidence=0.3
    )
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open camera. Please check your camera connection.")
        exit(1)
        
    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    
    # Get a test frame to check camera is working
    ret, frame = cap.read()
    if not ret:
        print("ERROR: Could not read frame from camera.")
        exit(1)
        
    print(f"Camera initialized. Frame size: {frame.shape}")
    print("Press 'q' to quit, 'c' to clear text")
    
    # Timing and stability settings
    letter_stable_time = 0
    letter_stable_threshold = 1.5
    last_stable_letter = ""
    current_letter = ""
    formed_text = ""
    
    # Two-hand space settings
    two_hands_detected = False
    two_hands_stable_time = 0
    two_hands_threshold = 0.5
    last_space_time = 0
    space_cooldown = 1.0
    
    # Main loop
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error reading from camera")
            break
            
        # Process the frame
        H, W, _ = frame.shape
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = hands.process(frame_rgb)
        current_time = time.time()
        
        if results.multi_hand_landmarks:
            num_hands = len(results.multi_hand_landmarks)
            
            if num_hands == 2:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )
                
                if not two_hands_detected:
                    two_hands_detected = True
                    two_hands_stable_time = current_time
                elif (current_time - two_hands_stable_time >= two_hands_threshold and 
                      current_time - last_space_time >= space_cooldown):
                    formed_text += " "
                    last_space_time = current_time
                    print(f"Current text: {formed_text}")
                    
                progress = min(1.0, (current_time - two_hands_stable_time) / two_hands_threshold)
                if progress < 1.0:
                    bar_width = int(200 * progress)
                    cv2.rectangle(frame, (W//2-100, 50), (W//2+100, 70), (0, 0, 255), 2)
                    cv2.rectangle(frame, (W//2-100, 50), (W//2-100+bar_width, 70), (0, 255, 0), -1)
                    cv2.putText(frame, "Hold for space", (W//2-100, 45),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
            
            else:
                two_hands_detected = False
                two_hands_stable_time = 0
                
                hand_landmarks = results.multi_hand_landmarks[0]
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
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
                
                prediction = model.predict([np.asarray(data_aux)])
                predicted_character = prediction[0]
                
                if predicted_character == last_stable_letter:
                    if letter_stable_time == 0:
                        letter_stable_time = current_time
                    
                    progress = min(1.0, (current_time - letter_stable_time) / letter_stable_threshold)
                    bar_width = int(100 * progress)
                    
                    x1 = int(min(x_) * W) - 10
                    y1 = int(min(y_) * H) - 10
                    x2 = int(max(x_) * W) - 10
                    y2 = int(max(y_) * H) - 10
                    
                    cv2.rectangle(frame, (x1, y1-30), (x1+100, y1-20), (0, 0, 255), 2)
                    cv2.rectangle(frame, (x1, y1-30), (x1+bar_width, y1-20), (0, 255, 0), -1)
                    
                    if current_time - letter_stable_time >= letter_stable_threshold:
                        formed_text += predicted_character
                        letter_stable_time = 0
                        print(f"Current text: {formed_text}")
                        
                    color = (0, 255, 0)
                    current_letter = predicted_character
                else:
                    last_stable_letter = predicted_character
                    letter_stable_time = 0
                    color = (0, 165, 255)
                    current_letter = predicted_character
                
                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10
                x2 = int(max(x_) * W) - 10
                y2 = int(max(y_) * H) - 10
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, predicted_character, (x1, y1 - 40),
                          cv2.FONT_HERSHEY_SIMPLEX, 1.3, color, 3, cv2.LINE_AA)
                
        # Instructions and current text display
        cv2.putText(frame, "Show two hands for space", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"Current letter: {current_letter}", (10, H - 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"Text: {formed_text}", (10, H - 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Display the frame
        cv2.imshow('Sign Language Detection (Standalone)', frame)
        
        # Key controls
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            formed_text = ""
            print("Text cleared")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    print("\nFinal text:", formed_text)
    
except Exception as e:
    print(f"ERROR: {str(e)}")
    print("The application encountered an error and had to close.") 