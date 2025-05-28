import cv2
import mediapipe as mp
import numpy as np
import os
import time

# Create directory for storing images
DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Initialize camera
cap = cv2.VideoCapture(0)
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Define labels (letters A-Z)
labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# Number of images to collect per label
number_imgs = 100

for label in labels:
    if not os.path.exists(os.path.join(DATA_DIR, label)):
        os.makedirs(os.path.join(DATA_DIR, label))

    print(f'Collecting images for {label}')
    print(f'Press "s" to start capturing {number_imgs} images')
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        
        # Draw label instructions
        cv2.putText(frame, f'Ready to collect images for "{label}"', (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, 'Press "s" to start', (20, 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        cv2.imshow('Frame', frame)
        
        # Wait for 's' key to start collection
        if cv2.waitKey(25) & 0xFF == ord('s'):
            break
            
    # Counter for current label
    counter = 0
    
    while counter < number_imgs:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = hands.process(frame_rgb)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                
            # Save the frame
            cv2.imwrite(os.path.join(DATA_DIR, label, f'{counter}.jpg'), frame)
            counter += 1
            
        # Show progress
        cv2.putText(frame, f'Collecting {counter}/{number_imgs} for "{label}"', (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    
        cv2.imshow('Frame', frame)
        cv2.waitKey(25)
        
    print(f'Collected {counter} images for {label}')

cap.release()
cv2.destroyAllWindows()
print("Image collection completed!") 