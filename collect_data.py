import cv2
import mediapipe as mp
import numpy as np
import os
import time

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Create directory for data
if not os.path.exists('data'):
    os.makedirs('data')

# Letters to collect
letters = ['C', 'G', 'K', 'M', 'N', 'R', 'S']
data_size = 100  # Number of samples per letter

cap = cv2.VideoCapture(0)

for letter in letters:
    counter = 0
    collecting = False  # Flag to control data collection
    
    print(f"\nReady to collect data for letter {letter}")
    print("Press 's' to start collecting, 'q' to quit")
    
    while counter < data_size:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        
        # Convert the BGR image to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame and detect hands
        results = hands.process(frame_rgb)
        
        if results.multi_hand_landmarks and collecting:
            # Get the first hand detected
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Draw the hand landmarks
            mp_drawing.draw_landmarks(
                frame, 
                hand_landmarks, 
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
            
            # Extract coordinates
            data_aux = []
            x_ = []
            y_ = []
            
            for landmark in hand_landmarks.landmark:
                x_.append(landmark.x)
                y_.append(landmark.y)
                
            # Normalize coordinates
            for landmark in hand_landmarks.landmark:
                data_aux.append(landmark.x - min(x_))
                data_aux.append(landmark.y - min(y_))
            
            # Save the data
            filename = os.path.join('data', f'{letter}_{counter}.npy')
            np.save(filename, data_aux)
            counter += 1
            
            # Visual feedback
            x1 = int(min(x_) * frame.shape[1]) - 10
            y1 = int(min(y_) * frame.shape[0]) - 10
            x2 = int(max(x_) * frame.shape[1]) - 10
            y2 = int(max(y_) * frame.shape[0]) - 10
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'{letter}: {counter}/{data_size}', (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
        
        # Display instructions
        if not collecting:
            cv2.putText(frame, f'Press "s" to start collecting letter: {letter}', (10, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, f'Collecting letter: {letter}', (10, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
        cv2.putText(frame, f'Progress: {counter}/{data_size}', (10, 100),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        cv2.imshow('Data Collection', frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            collecting = True
            print(f"Started collecting data for letter {letter}")
        elif key == ord('q'):
            break
            
    # Optional delay between letters
    if counter >= data_size:
        print(f'Completed collecting data for letter {letter}')
        time.sleep(2)

cap.release()
cv2.destroyAllWindows()
print("Data collection completed!") 