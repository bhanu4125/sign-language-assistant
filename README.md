# Sign Language Web Application

This web application provides real-time sign language detection and translation services through a web interface.

## Features
1. Sign Language to Text Conversion
2. Text to Sign Language Conversion
3. Multi-language Translation Support
4. Real-time Video Processing
5. Error Handling and Logging

## Prerequisites
- Python 3.8 or higher
- Webcam
- Modern web browser
- Git (for cloning the repository)

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Model File
Ensure the `model.p` file is present in the root directory. If not, you'll need to obtain it from the project maintainers.

## Running the Application

### Local Development
```bash
python app.py
```
The application will be available at `http://localhost:5000`

### Production Deployment

#### Using Gunicorn (Linux/macOS)
1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Using Waitress (Windows)
1. Install Waitress:
```bash
pip install waitress
```

2. Create a file named `waitress_server.py`:
```python
from waitress import serve
from app import app

serve(app, host='0.0.0.0', port=5000)
```

3. Run the server:
```bash
python waitress_server.py
```

## Directory Structure
```
.
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── model.p            # Trained model file
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
└── logs/             # Application logs
```

## Troubleshooting

### Camera Issues
1. Ensure no other application is using the webcam
2. Check browser permissions for camera access
3. Verify webcam is properly connected and working

### Model Loading Issues
1. Confirm `model.p` file exists in the root directory
2. Check logs in the `logs` directory for specific errors
3. Ensure all dependencies are properly installed

### Web Access Issues
1. Check if the server is running (look for "Running on http://..." message)
2. Verify firewall settings allow access to port 5000
3. Ensure you're using a supported browser (Chrome, Firefox, Edge recommended)

## Browser Support
- Google Chrome (recommended)
- Mozilla Firefox
- Microsoft Edge
- Safari

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
For support, please:
1. Check the logs in the `logs` directory
2. Create an issue in the repository
3. Contact the maintainers at [contact email] 