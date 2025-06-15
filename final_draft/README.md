# Sign Language Assistant (Final Version)

A desktop application for real-time sign language detection and translation. This application can convert sign language to text and includes features like multi-language translation and text-to-speech. This is the final, stable version with all dependencies properly configured.

## Features

- Real-time sign language detection using webcam
- Text-to-speech for both original and translated text
- Multi-language translation support (English, Telugu, Hindi, Tamil, German)
- Word suggestions and corrections
- Modern dark-themed GUI
- Space gesture recognition (show both hands)

## Prerequisites

- Python 3.8 or higher
- Webcam
- Windows OS (tested on Windows 10)
- Internet connection (for translation features)

## Installation

1. Extract all files to a directory of your choice
2. Run `setup.bat` to install required dependencies
3. Ensure `model.p` file is present in the same directory

## Usage

1. Run `launcher.py` to start the application
2. Click "Sign Language to Text" to open the detector
3. Show hand signs clearly in front of the camera
4. Hold a sign steady for 1.5 seconds to register a letter
5. Show both hands for adding a space
6. Use the GUI controls to:
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

All dependencies are automatically installed by setup.bat:
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
   - Verify `model.p` exists in the same directory as the application
   - Check if all dependencies are properly installed

3. Translation Issues:
   - Check internet connection
   - Verify the text is properly formed before translation

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.

## License

This project is licensed under the MIT License.
