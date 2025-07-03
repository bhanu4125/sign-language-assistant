# Sign Language Assistant

A desktop application for real-time sign language detection and translation. This application can convert sign language to text and includes features like multi-language translation and text-to-speech.

## Features

- Real-time sign language detection using webcam
- Text-to-speech for both original and translated text
- Multi-language translation support (English, Telugu, Hindi, Tamil, German)
- can able to speak the input text after the dection
- Word suggestions and corrections
- Modern dark-themed GUI
- Space gesture recognition (show both hands)

## Prerequisites

- Python 3.8 or higher
- Webcam
- Windows OS (tested on Windows 10)
- Internet connection (for translation features)

## Installation

1. Clone or download this repository
2. Run `setup.bat` to install required dependencies
3. Ensure `model.p` file is present in the root directory

## Usage

1. Run `inference_classifier.py` to start the application
2. Show hand signs clearly in front of the camera
3. Hold a sign steady for 1.5 seconds to register a letter
4. Show both hands for adding a space
5. Use the GUI controls to:
   - Clear text
   - Speak text (original/translated)
   - Change translation language
   - Select word suggestions

## Supported Languages

- English (default)
- Telugu
- Hindi
- Tamil
- German

## Dependencies

- opencv-python
- mediapipe
- numpy
- customtkinter
- pyttsx3
- Pillow
- deep-translator
- textblob

## Troubleshooting

1. Camera Issues:
   - Ensure no other application is using the webcam
   - Check if webcam is properly connected
   - Verify camera permissions

2. Model Loading Issues:
   - Verify `model.p` exists in the root directory
   - Check if all dependencies are properly installed

3. Translation Issues:
   - Check internet connection
   - Verify the text is properly formed before translation

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.

## License

This project is licensed under the MIT License.
