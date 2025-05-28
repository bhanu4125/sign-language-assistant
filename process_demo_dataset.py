import cv2
import mediapipe as mp
import numpy as np
import os

def process_demo_dataset():
    # Initialize MediaPipe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=1,
        min_detection_confidence=0.5
    )
    
    # Letters that we already have data for
    keep_letters = {'C', 'G', 'K', 'M', 'N', 'R', 'S'}
    # Letters to process from demo_dataset
    letters_to_process = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ') - keep_letters
    
    total_processed = 0
    failed_images = 0
    
    print("Processing demo dataset...")
    print("-" * 50)
    
    for letter in letters_to_process:
        source_dir = os.path.join('demo_dataset', letter)
        if not os.path.exists(source_dir):
            print(f"Directory not found for letter {letter}")
            continue
            
        print(f"\nProcessing letter {letter}...")
        processed_count = 0
        
        # Get list of jpg files
        image_files = [f for f in os.listdir(source_dir) if f.endswith('.jpg')]
        
        for i, image_file in enumerate(image_files):
            source_path = os.path.join(source_dir, image_file)
            
            # Read and process image
            image = cv2.imread(source_path)
            if image is None:
                print(f"Failed to read image: {source_path}")
                failed_images += 1
                continue
                
            # Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            results = hands.process(image_rgb)
            
            if results.multi_hand_landmarks:
                # Get the first hand detected
                hand_landmarks = results.multi_hand_landmarks[0]
                
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
                
                # Save as npy file
                output_path = os.path.join('data', f'{letter}_{i}.npy')
                np.save(output_path, data_aux)
                processed_count += 1
                total_processed += 1
            else:
                print(f"No hand landmarks detected in {image_file}")
                failed_images += 1
        
        print(f"Processed {processed_count} images for letter {letter}")
    
    print("\nProcessing Complete!")
    print("-" * 50)
    print(f"Total images processed successfully: {total_processed}")
    print(f"Total images failed: {failed_images}")
    
    # Print final dataset summary
    print("\nFinal Dataset Summary:")
    print("-" * 50)
    letter_counts = {}
    for file in os.listdir('data'):
        letter = file[0]
        letter_counts[letter] = letter_counts.get(letter, 0) + 1
    
    print("Letter | Count")
    print("-" * 50)
    for letter in sorted(letter_counts.keys()):
        print(f"   {letter}   |  {letter_counts[letter]}")

if __name__ == "__main__":
    process_demo_dataset() 