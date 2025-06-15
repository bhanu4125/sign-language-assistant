import os
import shutil
from pathlib import Path

def copy_website_files():
    # Source directory (where the website files are)
    source_dir = r"C:\Users\tumma\OneDrive\Desktop\safe\project"
    
    # Destination directory (current project directory)
    dest_dir = os.path.dirname(os.path.abspath(__file__))
    website_dir = os.path.join(dest_dir, "website")
    
    print("Starting website files copy...")
    
    try:
        # Create website directory if it doesn't exist
        if os.path.exists(website_dir):
            shutil.rmtree(website_dir)  # Remove existing website directory
        os.makedirs(website_dir)
        
        # Copy everything from source directory
        for item in os.listdir(source_dir):
            source_path = os.path.join(source_dir, item)
            dest_path = os.path.join(website_dir, item)
            
            if os.path.isdir(source_path):
                shutil.copytree(source_path, dest_path)
                print(f"Copied directory: {item}")
            else:
                shutil.copy2(source_path, dest_path)
                print(f"Copied file: {item}")
        
        # Create a simple server script to serve the website
        server_script = os.path.join(website_dir, "serve.py")
        with open(server_script, "w") as f:
            f.write("""
import http.server
import socketserver
import os
import webbrowser
from threading import Thread
import time

def start_server():
    PORT = 8000
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving website at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    # Start server in a separate thread
    server_thread = Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Open browser after a short delay
    time.sleep(1)
    webbrowser.open("http://localhost:8000")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\\nServer stopped.")
""")
        print(f"Created server script: serve.py")
        
        print("\nWebsite files copied successfully!")
        print(f"Files are located in: {website_dir}")
        print("\nTo start the website server, run: python website/serve.py")
        
    except Exception as e:
        print(f"Error copying files: {str(e)}")

if __name__ == "__main__":
    copy_website_files() 