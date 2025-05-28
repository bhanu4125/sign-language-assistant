import pickle
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def load_data():
    data_dict = {
        'data': [],
        'labels': []
    }
    
    # Process all letters A-Z
    letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    
    # Load the data from the data directory
    for letter in letters:
        data_files = [f for f in os.listdir('data') if f.startswith(f'{letter}_') and f.endswith('.npy')]
        
        for file in data_files:
            try:
                data_point = np.load(os.path.join('data', file))
                data_dict['data'].append(data_point)
                data_dict['labels'].append(letter)
            except Exception as e:
                print(f"Error loading file {file}: {e}")
    
    return np.array(data_dict['data']), np.array(data_dict['labels'])

def train_model():
    print("Loading data...")
    X, y = load_data()
    
    if len(X) == 0:
        print("No data found! Please run data collection first.")
        return
    
    print(f"\nDataset summary:")
    print(f"Total samples: {len(X)}")
    for letter in sorted(np.unique(y)):
        count = len(y[y == letter])
        print(f"Letter {letter}: {count} samples")
    
    # Split the data into training and testing sets
    print("\nSplitting data into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and train the model
    print("\nTraining Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate the model
    print("\nEvaluating model performance...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy * 100:.2f}%")
    
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model
    print("\nSaving model...")
    data = {
        'model': model,
        'letters': sorted(list(np.unique(y)))
    }
    with open('model.p', 'wb') as f:
        pickle.dump(data, f)
    
    print("Model saved as 'model.p'")

if __name__ == "__main__":
    train_model() 