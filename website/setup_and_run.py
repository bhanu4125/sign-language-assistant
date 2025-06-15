import os
import subprocess
import sys
import time
import re

def find_executable(name):
    print(f"Searching for {name}...")
    # Common Node.js installation path on Windows
    possible_paths = [
        os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'), 'nodejs', name),
        os.path.join(os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'), 'nodejs', name),
        os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'npm', name), # For npm on some installs
        os.path.join(os.environ.get('APPDATA', ''), 'npm', name) # For npm on some installs, APPDATA might be better than ~\AppData\Roaming
    ]
    
    # Also check current environment PATH
    print(f"Checking PATH environment variable: {os.environ.get('PATH', 'PATH not set')}")
    for path_dir in os.environ['PATH'].split(os.pathsep):
        full_path = os.path.join(path_dir, name)
        if os.path.isfile(full_path):
            print(f"Found {name} in PATH: {full_path}")
            return full_path
            
    for path in possible_paths:
        if os.path.isfile(path):
            print(f"Found {name} in common path: {path}")
            return path
    print(f"{name} not found in any checked locations.")
    return None

def check_node_npm_installed():
    node_path = find_executable("node.exe")
    npm_path = find_executable("npm.cmd")
    
    if not node_path or not npm_path:
        print("Error: Node.js or npm is not installed or not found in common locations/PATH.")
        print("Please install Node.js from https://nodejs.org/ and ensure it's added to your system's PATH.")
        input("Press Enter to close this window...")
        return False, None, None
    
    print(f"Node.js executable found at: {node_path}")
    print(f"npm executable found at: {npm_path}")
    return True, node_path, npm_path

def run_command_capture_output(command_parts, cwd):
    print(f"\nRunning command: {' '.join(command_parts)} in directory: {cwd}")
    print(f"Environment PATH for command: {os.environ.get('PATH', 'PATH not set')}")
    try:
        process = subprocess.Popen(command_parts, cwd=cwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NEW_CONSOLE, env=os.environ)
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            print(f"Error running command {' '.join(command_parts)}:")
            print("STDOUT:", stdout)
            print("STDERR:", stderr)
            return False, stdout, stderr
        print("STDOUT:", stdout)
        print("STDERR:", stderr)
        return True, stdout, stderr
    except Exception as e:
        print(f"An error occurred while running command {' '.join(command_parts)}: {e}")
        return False, "", str(e)

def setup_and_run():
    website_dir = os.path.dirname(os.path.abspath(__file__))

    print("Starting website preview server setup...")
    print(f"Current working directory of script: {os.getcwd()}")
    print(f"Script is located at: {os.path.abspath(__file__)}")
    
    is_installed, node_path, npm_path = check_node_npm_installed()
    if not is_installed:
        return
    
    npm_cmd_parts = [npm_path]

    if not os.path.exists(os.path.join(website_dir, 'node_modules')):
        print("node_modules not found. Running npm install...")
        success, _, _ = run_command_capture_output(npm_cmd_parts + ["install"], website_dir)
        if not success:
            print("Failed to install dependencies. Please try running 'npm install' manually in the website directory.")
            input("Press Enter to close this window...")
            return

    if not os.path.exists(os.path.join(website_dir, 'dist')):
        print("dist folder not found. Running npm run build...")
        success, _, _ = run_command_capture_output(npm_cmd_parts + ["run", "build"], website_dir)
        if not success:
            print("Failed to build the project. Please try running 'npm run build' manually in the website directory.")
            input("Press Enter to close this window...")
            return

    print("\nAttempting to start Vite preview server...")

    try:
        # Start the preview server in the background and capture its output to get the URL
        process = subprocess.Popen(npm_cmd_parts + ["run", "preview"], cwd=website_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NEW_CONSOLE, env=os.environ)
        
        local_url = None
        print("Waiting for server to start and provide URL...")
        # Read stdout line by line to find the URL
        for line in iter(process.stdout.readline, ''):
            print(line, end='') # Print output to the console for user visibility
            match = re.search(r"Local:\s*(http://localhost:\d+/?)", line)
            if match:
                local_url = match.group(1)
                print(f"Found server URL: {local_url}")
                # Print the URL in a recognizable format for the launcher to capture
                print(f"__SERVER_URL__:{local_url}") 
                break # Found the URL, stop reading stdout for it

        if not local_url:
            print("Error: Could not find local server URL in output.")
            
        print(f"Server process started with PID: {process.pid}")
        print("You can close this window after the website loads. If it doesn't load, check for errors above.")
        
        process.wait() # Keep this console window open until user closes it or server process ends

    except Exception as e:
        print(f"Failed to start preview server: {e}")
        print("Please ensure Node.js is installed and dependencies are met, then try running 'npm run preview' manually in the website directory.")
    
    input("Press Enter to close this window...") # Ensure window stays open for debugging

if __name__ == "__main__":
    setup_and_run() 