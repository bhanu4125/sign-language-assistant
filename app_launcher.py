import subprocess
import os
import sys
import webbrowser

def launch_sign_to_text():
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inference_classifier.py")
    subprocess.Popen([sys.executable, script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)

def launch_text_to_sign():
    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "text_to_sign.html")
    webbrowser.open(f'file:///{html_path}')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "sign-to-text":
            launch_sign_to_text()
        elif sys.argv[1] == "text-to-sign":
            launch_text_to_sign() 