from flask import Flask, render_template, jsonify
import subprocess
import os
import sys

app = Flask(__name__)

# Configure paths - using absolute paths with proper escaping
DTI2_PATH = os.path.abspath(r"C:\Users\tumma\OneDrive\Documents\2nd chance\dti 2")
TEXT_TO_SIGN_PATH = os.path.abspath(r"C:\Users\tumma\OneDrive\Documents\2nd chance\text to sign")  # Updated path
PYTHON_PATH = sys.executable

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/launch/<app_name>')
def launch_app(app_name):
    try:
        if app_name == 'dti2':
            if not os.path.exists(os.path.join(DTI2_PATH, 'inference_classifier.py')):
                return jsonify({'status': 'error', 'message': f'Could not find inference_classifier.py in {DTI2_PATH}'})
            
            process = subprocess.Popen(
                [PYTHON_PATH, 'inference_classifier.py'],
                cwd=DTI2_PATH,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            return jsonify({'status': 'success', 'message': 'Sign to Text application launched successfully'})
        
        elif app_name == 'text-to-sign':
            if not os.path.exists(os.path.join(TEXT_TO_SIGN_PATH, 'main.py')):
                return jsonify({'status': 'error', 'message': f'Could not find main.py in {TEXT_TO_SIGN_PATH}'})
            
            process = subprocess.Popen(
                [PYTHON_PATH, 'main.py'],
                cwd=TEXT_TO_SIGN_PATH,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            return jsonify({'status': 'success', 'message': 'Text to Sign application launched successfully'})
        
        else:
            return jsonify({'status': 'error', 'message': 'Invalid application name'})
    
    except Exception as e:
        error_msg = f"""Error: {str(e)}
Python Path: {PYTHON_PATH}
Working Directory: {os.getcwd()}
DTI2 Path: {DTI2_PATH} (exists: {os.path.exists(DTI2_PATH)})
Text-to-Sign Path: {TEXT_TO_SIGN_PATH} (exists: {os.path.exists(TEXT_TO_SIGN_PATH)})"""
        print(error_msg)  # Print to server console for debugging
        return jsonify({'status': 'error', 'message': error_msg})

if __name__ == '__main__':
    try:
        # Print debug information
        print(f"Python Executable: {PYTHON_PATH}")
        print(f"Current Working Directory: {os.getcwd()}")
        print(f"DTI2 Path exists: {os.path.exists(DTI2_PATH)}")
        print(f"Text-to-Sign Path exists: {os.path.exists(TEXT_TO_SIGN_PATH)}")
        
        # Create templates directory if it doesn't exist
        if not os.path.exists('templates'):
            os.makedirs('templates')
        
        # Move index.html to templates if it's not there
        if not os.path.exists('templates/index.html') and os.path.exists('index.html'):
            os.rename('index.html', 'templates/index.html')
        
        # Run the Flask app on all interfaces
        print("Starting server on http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        input("Press Enter to exit...") 