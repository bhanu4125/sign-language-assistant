class SignLanguageDetector {
    constructor() {
        this.model = null;
        this.hands = null;
        this.mp_hands = null;
        this.mp_drawing = null;
        this.mp_drawing_styles = null;
        
        this.letterStableTime = 0;
        this.letterStableThreshold = 1.5;
        this.lastStableLetter = "";
        this.currentLetter = "";
        
        this.onLetterDetected = null;
        this.onTextUpdated = null;
        
        this.isRunning = false;
    }
    
    async initialize() {
        try {
            // Load MediaPipe
            this.mp_hands = window.mediapipe.solutions.hands;
            this.mp_drawing = window.mediapipe.solutions.drawing_utils;
            this.mp_drawing_styles = window.mediapipe.solutions.drawing_styles;
            
            // Initialize hands detection
            this.hands = new this.mp_hands.Hands({
                staticImageMode: false,
                maxNumHands: 2,
                minDetectionConfidence: 0.3,
                minTrackingConfidence: 0.3
            });
            
            // Load the model
            const response = await fetch('model.p');
            const modelData = await response.json();
            this.model = modelData.model;
            
            return true;
        } catch (err) {
            console.error('Error initializing detector:', err);
            return false;
        }
    }
    
    start() {
        if (!this.isRunning) {
            this.isRunning = true;
            this.processFrames();
        }
    }
    
    stop() {
        this.isRunning = false;
    }
    
    processFrames() {
        if (!this.isRunning) return;
        
        const video = document.getElementById('camera-feed');
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        const processFrame = () => {
            if (!this.isRunning) return;
            
            ctx.drawImage(video, 0, 0);
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            
            this.processImage(imageData);
            
            requestAnimationFrame(processFrame);
        };
        
        requestAnimationFrame(processFrame);
    }
    
    processImage(imageData) {
        const results = this.hands.process(imageData);
        
        if (results.multiHandLandmarks) {
            const landmarks = results.multiHandLandmarks[0];
            if (landmarks) {
                const prediction = this.predictLetter(landmarks);
                this.updateLetterState(prediction);
            }
        }
    }
    
    predictLetter(landmarks) {
        // Convert landmarks to the format expected by the model
        const data = [];
        const x = [];
        const y = [];
        
        landmarks.forEach(landmark => {
            x.push(landmark.x);
            y.push(landmark.y);
        });
        
        landmarks.forEach(landmark => {
            data.push(landmark.x - Math.min(...x));
            data.push(landmark.y - Math.min(...y));
        });
        
        // Make prediction using the model
        return this.model.predict([data])[0];
    }
    
    updateLetterState(predictedLetter) {
        const currentTime = Date.now() / 1000;
        
        if (predictedLetter === this.lastStableLetter) {
            if (this.letterStableTime === 0) {
                this.letterStableTime = currentTime;
            }
            
            if (currentTime - this.letterStableTime >= this.letterStableThreshold) {
                if (this.onLetterDetected) {
                    this.onLetterDetected(predictedLetter);
                }
                this.letterStableTime = 0;
            }
        } else {
            this.lastStableLetter = predictedLetter;
            this.letterStableTime = 0;
            
            if (this.onLetterDetected) {
                this.onLetterDetected(predictedLetter);
            }
        }
    }
    
    setCallbacks(onLetterDetected, onTextUpdated) {
        this.onLetterDetected = onLetterDetected;
        this.onTextUpdated = onTextUpdated;
    }
}

// Export the class
window.SignLanguageDetector = SignLanguageDetector; 