from flask import Flask, render_template, Response, jsonify, send_from_directory
import cv2
import mediapipe as mp
import numpy as np
import pickle
from deep_translator import GoogleTranslator
import os
import sys
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variables for letter detection
letter_stable_time = 0
letter_stable_threshold = 1.5
last_stable_letter = ""
current_letter = ""
formed_text = ""

try:
    # Load the DTI2 model
    model_path = os.path.join(os.path.dirname(__file__), 'model.p')
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    
    model_dict = pickle.load(open(model_path, 'rb'))
    model = model_dict['model']
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    model = None

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.3,
    min_tracking_confidence=0.3
)

def generate_frames():
    camera = None
    try:
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            raise Exception("Could not open camera")
        
        while True:
            success, frame = camera.read()
            if not success:
                break
            
            # Process frame for hand detection
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
                        mp_drawing_styles.get_default_hand_connections_style()
                    )
                    
                    if model is not None:
                        # Process landmarks for prediction
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
                        
                        # Draw prediction on frame
                        x1 = int(min(x_) * frame.shape[1]) - 10
                        y1 = int(min(y_) * frame.shape[0]) - 10
                        
                        cv2.putText(frame, predicted_character, (x1, y1 - 10),
                                  cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3,
                                  cv2.LINE_AA)
            
            # Convert frame to jpg
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except Exception as e:
        logger.error(f"Error in generate_frames: {str(e)}")
        if camera is not None:
            camera.release()
        yield b''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_text')
def get_text():
    global formed_text
    return jsonify({'text': formed_text})

@app.route('/translate/<text>/<lang>')
def translate_text(text, lang):
    try:
        translator = GoogleTranslator(source='en', target=lang)
        translated = translator.translate(text)
        return jsonify({'translated': translated})
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/text_to_sign')
def text_to_sign():
    return render_template('text_to_sign.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Add file handler for logging
    file_handler = logging.FileHandler(
        f'logs/app_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=True) 