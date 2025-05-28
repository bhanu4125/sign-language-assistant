import http.server
import socketserver
import json
import subprocess
import os
import sys

# Configure paths
DTI2_PATH = os.path.abspath(r"C:\Users\tumma\OneDrive\Documents\2nd chance\dti 2")
TEXT_TO_SIGN_PATH = os.path.abspath(r"C:\Users\tumma\OneDrive\Documents\2nd chance\text to sign")
PYTHON_PATH = sys.executable

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        
        elif self.path.startswith('/launch/'):
            app_name = self.path.split('/')[-1]
            try:
                if app_name == 'dti2':
                    subprocess.Popen(
                        [PYTHON_PATH, 'inference_classifier.py'],
                        cwd=DTI2_PATH,
                        creationflags=subprocess.CREATE_NEW_CONSOLE
                    )
                    response = {'status': 'success', 'message': 'Sign to Text application launched successfully'}
                
                elif app_name == 'text-to-sign':
                    subprocess.Popen(
                        [PYTHON_PATH, 'main.py'],
                        cwd=TEXT_TO_SIGN_PATH,
                        creationflags=subprocess.CREATE_NEW_CONSOLE
                    )
                    response = {'status': 'success', 'message': 'Text to Sign application launched successfully'}
                
                else:
                    response = {'status': 'error', 'message': 'Invalid application name'}
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                return
                
            except Exception as e:
                response = {'status': 'error', 'message': str(e)}
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                return
        
        else:
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

def run_server():
    PORT = 8000  # Using port 8000 instead of 5000
    
    print(f"Starting server...")
    print(f"Python Executable: {PYTHON_PATH}")
    print(f"Current Directory: {os.getcwd()}")
    print(f"DTI2 Path exists: {os.path.exists(DTI2_PATH)}")
    print(f"Text-to-Sign Path exists: {os.path.exists(TEXT_TO_SIGN_PATH)}")
    
    with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
        print(f"\nServer started!")
        print(f"Open your web browser and go to:")
        print(f"http://localhost:{PORT}")
        print(f"http://127.0.0.1:{PORT}")
        print("\nPress Ctrl+C to stop the server.")
        httpd.serve_forever()

if __name__ == '__main__':
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"\nError: {str(e)}")
        input("Press Enter to exit...") 