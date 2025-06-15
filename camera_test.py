import cv2
import os
import sys

def test_camera():
    print("Testing camera access...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ERROR: Could not open camera. Please check your camera connection.")
        return False
    
    ret, frame = cap.read()
    if not ret:
        print("ERROR: Could not read frame from camera.")
        return False
    
    print(f"SUCCESS: Camera is working. Frame size: {frame.shape}")
    
    # Save a test frame
    cv2.imwrite("camera_test.jpg", frame)
    print(f"Saved test image to {os.path.abspath('camera_test.jpg')}")
    
    # Release camera
    cap.release()
    return True

def test_dependencies():
    print("\nTesting dependencies...")
    try:
        import mediapipe as mp
        print("SUCCESS: mediapipe is installed")
    except ImportError:
        print("ERROR: mediapipe is not installed correctly")
        return False
    
    try:
        import pickle
        print("SUCCESS: pickle is installed")
    except ImportError:
        print("ERROR: pickle is not installed correctly")
        return False
        
    try:
        import numpy as np
        print("SUCCESS: numpy is installed")
    except ImportError:
        print("ERROR: numpy is not installed correctly")
        return False
    
    try:
        import customtkinter
        print("SUCCESS: customtkinter is installed")
    except ImportError:
        print("ERROR: customtkinter is not installed correctly")
        return False
    
    try:
        from PIL import Image, ImageTk
        print("SUCCESS: PIL is installed")
    except ImportError:
        print("ERROR: PIL is not installed correctly")
        return False
    
    try:
        from deep_translator import GoogleTranslator
        print("SUCCESS: deep_translator is installed")
    except ImportError:
        print("ERROR: deep_translator is not installed correctly")
        return False
    
    return True

def test_model():
    print("\nTesting model file...")
    model_path = './model.p'
    
    if not os.path.exists(model_path):
        print(f"ERROR: Model file not found at {os.path.abspath(model_path)}")
        return False
    
    try:
        import pickle
        model_dict = pickle.load(open(model_path, 'rb'))
        model = model_dict['model']
        print(f"SUCCESS: Model loaded successfully")
        return True
    except Exception as e:
        print(f"ERROR: Failed to load model: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Sign Language Detection System Test ===")
    print(f"Python version: {sys.version}")
    print(f"OpenCV version: {cv2.__version__}")
    print(f"Current directory: {os.getcwd()}")
    
    camera_ok = test_camera()
    deps_ok = test_dependencies()
    model_ok = test_model()
    
    print("\n=== Test Summary ===")
    print(f"Camera: {'OK' if camera_ok else 'FAILED'}")
    print(f"Dependencies: {'OK' if deps_ok else 'FAILED'}")
    print(f"Model: {'OK' if model_ok else 'FAILED'}")
    
    if camera_ok and deps_ok and model_ok:
        print("\nAll tests passed! The system should be ready to run.")
    else:
        print("\nSome tests failed. Please fix the issues before running the application.")
    
    input("\nPress Enter to exit...") 