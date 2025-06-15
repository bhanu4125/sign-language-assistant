import cv2
import mediapipe as mp
import numpy as np
import pickle
import os

def main():
    print("Starting minimal sign language detector...")
    
    # Check if model exists
    if not os.path.exists('model.p'):
        print("Error: model.p not found in current directory")
        return
    
    # Load model
    try:
        model_dict = pickle.load(open('model.p', 'rb'))
        model = model_dict['model']
        print("Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        return
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    # Initialize MediaPipe
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2,
                         min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    print("\nInstructions:")
    print("1. Show hand signs clearly in front of the camera")
    print("2. Hold the sign steady to detect letters")
    print("3. Show both hands for space")
    print("4. Press 'q' to quit")
    print("5. Press 'c' to clear text")
    print("\nStarting camera feed...")
    
    # Initialize text formation
    text = ""
    
    while True:
        # Read frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Couldn't read frame")
            break
        
        # Flip and convert
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process hands
        results = hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            # Get number of hands
            num_hands = len(results.multi_hand_landmarks)
            
            # Handle space (two hands)
            if num_hands == 2:
                text += " "
                cv2.putText(frame, "SPACE", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            
            # Handle single hand (letter detection)
            elif num_hands == 1:
                # Get hand landmarks
                hand = results.multi_hand_landmarks[0]
                
                # Draw landmarks
                mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
                
                # Extract coordinates
                data_aux = []
                x_ = []
                y_ = []
                
                for landmark in hand.landmark:
                    x_.append(landmark.x)
                    y_.append(landmark.y)
                
                for landmark in hand.landmark:
                    data_aux.append(landmark.x - min(x_))
                    data_aux.append(landmark.y - min(y_))
                
                # Predict
                prediction = model.predict([np.asarray(data_aux)])
                predicted_char = prediction[0]
                
                # Add character to text
                text += predicted_char
                
                # Draw prediction
                cv2.putText(frame, predicted_char, (10, 50), 
                          cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0,255,0), 2)
        
        # Show text
        cv2.putText(frame, f"Text: {text}", (10, frame.shape[0] - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
        
        # Show frame
        cv2.imshow("Sign Language Detection", frame)
        
        # Handle keys
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('c'):
            text = ""
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("\nFinal text:", text)

if __name__ == "__main__":
    main() 