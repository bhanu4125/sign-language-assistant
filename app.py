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
import time
from textblob import Word

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class SignLanguageDetector:
    def __init__(self):
        # Initialize model and MediaPipe
        self.model_dict = pickle.load(open('./model.p', 'rb'))
        self.model = self.model_dict['model']
        
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
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
        self.formed_text = ""
        
        # Two-hand space settings
        self.two_hands_detected = False
        self.two_hands_stable_time = 0
        self.two_hands_threshold = 0.5
        self.last_space_time = 0
        self.space_cooldown = 1.0

detector = SignLanguageDetector()

def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # Flip frame horizontally
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = detector.hands.process(frame_rgb)
        current_time = time.time()
        
        if results.multi_hand_landmarks:
            num_hands = len(results.multi_hand_landmarks)
            
            if num_hands == 2:
                for hand_landmarks in results.multi_hand_landmarks:
                    detector.mp_drawing.draw_landmarks(
                        frame, hand_landmarks, detector.mp_hands.HAND_CONNECTIONS,
                        detector.mp_drawing_styles.get_default_hand_landmarks_style(),
                        detector.mp_drawing_styles.get_default_hand_connections_style()
                    )
                
                if not detector.two_hands_detected:
                    detector.two_hands_detected = True
                    detector.two_hands_stable_time = current_time
                elif (current_time - detector.two_hands_stable_time >= detector.two_hands_threshold and 
                      current_time - detector.last_space_time >= detector.space_cooldown):
                    detector.formed_text += " "
                    detector.last_space_time = current_time
            else:
                detector.two_hands_detected = False
                detector.two_hands_stable_time = 0
                
                hand_landmarks = results.multi_hand_landmarks[0]
                detector.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, detector.mp_hands.HAND_CONNECTIONS,
                    detector.mp_drawing_styles.get_default_hand_landmarks_style(),
                    detector.mp_drawing_styles.get_default_hand_connections_style()
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
                
                prediction = detector.model.predict([np.asarray(data_aux)])
                predicted_character = prediction[0]
                
                if predicted_character == detector.last_stable_letter:
                    if detector.letter_stable_time == 0:
                        detector.letter_stable_time = current_time
                    
                    if current_time - detector.letter_stable_time >= detector.letter_stable_threshold:
                        detector.formed_text += predicted_character
                        detector.letter_stable_time = 0
                else:
                    detector.last_stable_letter = predicted_character
                    detector.letter_stable_time = 0
                
                x1 = int(min(x_) * frame.shape[1]) - 10
                y1 = int(min(y_) * frame.shape[0]) - 10
                
                cv2.putText(frame, predicted_character, (x1, y1 - 40),
                          cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html', text=detector.formed_text)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_text')
def get_text():
    return {'text': detector.formed_text}

@app.route('/clear_text')
def clear_text():
    detector.formed_text = ""
    return {'status': 'success'}

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