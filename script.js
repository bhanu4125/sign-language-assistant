// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Navbar scroll effect
const navbar = document.querySelector('.navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll <= 0) {
        navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        return;
    }
    
    if (currentScroll > lastScroll) {
        // Scrolling down
        navbar.style.transform = 'translateY(-100%)';
    } else {
        // Scrolling up
        navbar.style.transform = 'translateY(0)';
        navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    }
    
    lastScroll = currentScroll;
});

// Form submission handling
const contactForm = document.querySelector('.contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(this);
        const data = Object.fromEntries(formData);
        
        // Show submission feedback
        const submitBtn = this.querySelector('.submit-btn');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Sending...';
        
        // Simulate form submission (replace with actual API call)
        setTimeout(() => {
            submitBtn.textContent = 'Message Sent!';
            this.reset();
            
            setTimeout(() => {
                submitBtn.textContent = originalText;
            }, 2000);
        }, 1500);
    });
}

// Intersection Observer for animations
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.feature-card, .step, .demo-card').forEach(el => {
    observer.observe(el);
});

// Mobile menu toggle
const createMobileMenu = () => {
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelector('.nav-links');
    
    // Create hamburger menu button
    const menuBtn = document.createElement('button');
    menuBtn.classList.add('mobile-menu-btn');
    menuBtn.innerHTML = '<i class="fas fa-bars"></i>';
    
    // Add mobile menu button to navbar
    navbar.appendChild(menuBtn);
    
    // Toggle menu on click
    menuBtn.addEventListener('click', () => {
        navLinks.classList.toggle('show');
        menuBtn.classList.toggle('active');
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!navbar.contains(e.target)) {
            navLinks.classList.remove('show');
            menuBtn.classList.remove('active');
        }
    });
};

// Initialize mobile menu
if (window.innerWidth <= 768) {
    createMobileMenu();
}

// Demo videos autoplay on hover
document.querySelectorAll('.demo-video video').forEach(video => {
    video.addEventListener('mouseenter', () => {
        video.play();
    });
    
    video.addEventListener('mouseleave', () => {
        video.pause();
        video.currentTime = 0;
    });
});

// Add loading animation for download buttons
document.querySelectorAll('.download-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        
        const originalText = this.textContent;
        this.textContent = 'Preparing Download...';
        
        // Simulate download preparation (replace with actual download logic)
        setTimeout(() => {
            this.textContent = 'Starting Download...';
            // Trigger actual download here
            setTimeout(() => {
                this.textContent = originalText;
            }, 1500);
        }, 1500);
    });
});

// Add scroll to top button
const createScrollTopButton = () => {
    const button = document.createElement('button');
    button.classList.add('scroll-top');
    button.innerHTML = '<i class="fas fa-arrow-up"></i>';
    document.body.appendChild(button);
    
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 500) {
            button.classList.add('show');
        } else {
            button.classList.remove('show');
        }
    });
    
    button.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
};

createScrollTopButton();

// Add CSS for new elements
const style = document.createElement('style');
style.textContent = `
    .mobile-menu-btn {
        display: none;
        background: none;
        border: none;
        font-size: 1.5rem;
        color: var(--primary-color);
        cursor: pointer;
        padding: 0.5rem;
    }
    
    @media (max-width: 768px) {
        .mobile-menu-btn {
            display: block;
        }
        
        .nav-links.show {
            display: flex;
            flex-direction: column;
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: var(--white);
            padding: 1rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
    }
    
    .scroll-top {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: var(--primary-color);
        color: var(--white);
        width: 40px;
        height: 40px;
        border-radius: 50%;
        border: none;
        cursor: pointer;
        opacity: 0;
        transform: translateY(100px);
        transition: all 0.3s;
    }
    
    .scroll-top.show {
        opacity: 1;
        transform: translateY(0);
    }
    
    .scroll-top:hover {
        background: var(--secondary-color);
    }
    
    .feature-card,
    .step,
    .demo-card {
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.6s;
    }
    
    .feature-card.animate,
    .step.animate,
    .demo-card.animate {
        opacity: 1;
        transform: translateY(0);
    }
`;

document.head.appendChild(style);

// Sign to Text Integration
class SignToTextApp {
    constructor() {
        this.camera = document.getElementById('camera-feed');
        this.currentLetter = document.getElementById('current-letter');
        this.formedText = document.getElementById('formed-text');
        this.translatedText = document.getElementById('translated-text');
        this.startButton = document.getElementById('start-camera');
        this.clearButton = document.getElementById('clear-text');
        this.languageSelect = document.getElementById('translation-language');
        this.wordSuggestions = document.getElementById('word-suggestions');
        
        this.detector = null;
        this.stream = null;
        
        this.setupEventListeners();
    }
    
    async setupEventListeners() {
        this.startButton.addEventListener('click', () => this.toggleCamera());
        this.clearButton.addEventListener('click', () => this.clearText());
        this.languageSelect.addEventListener('change', () => this.updateTranslation());
    }
    
    async toggleCamera() {
        if (!this.stream) {
            try {
                this.stream = await navigator.mediaDevices.getUserMedia({ video: true });
                this.camera.srcObject = this.stream;
                this.camera.play();
                this.startButton.textContent = 'Stop Camera';
                
                // Initialize sign language detector
                this.detector = new SignLanguageDetector();
                this.detector.start();
                
            } catch (err) {
                console.error('Error accessing camera:', err);
                alert('Could not access camera. Please check permissions.');
            }
        } else {
            this.stream.getTracks().forEach(track => track.stop());
            this.camera.srcObject = null;
            this.stream = null;
            this.startButton.textContent = 'Start Camera';
            
            if (this.detector) {
                this.detector.stop();
                this.detector = null;
            }
        }
    }
    
    clearText() {
        this.formedText.textContent = '';
        this.translatedText.textContent = '';
        this.updateWordSuggestions('');
    }
    
    updateTranslation() {
        const text = this.formedText.textContent;
        if (text) {
            const targetLang = this.languageSelect.value;
            this.translateText(text, targetLang);
        }
    }
    
    async translateText(text, targetLang) {
        try {
            const translator = new GoogleTranslator({
                source: 'en',
                target: targetLang
            });
            const translatedText = await translator.translate(text);
            this.translatedText.textContent = translatedText;
        } catch (err) {
            console.error('Translation error:', err);
            this.translatedText.textContent = 'Translation error occurred';
        }
    }
    
    updateWordSuggestions(word) {
        // Clear previous suggestions
        this.wordSuggestions.innerHTML = '';
        
        if (word) {
            // Get word suggestions (implement your suggestion logic here)
            const suggestions = this.getWordSuggestions(word);
            suggestions.forEach(suggestion => {
                const btn = document.createElement('button');
                btn.className = 'suggestion-btn';
                btn.textContent = suggestion;
                btn.addEventListener('click', () => this.useSuggestion(suggestion));
                this.wordSuggestions.appendChild(btn);
            });
        }
    }
    
    useSuggestion(suggestion) {
        const words = this.formedText.textContent.split(' ');
        words[words.length - 1] = suggestion;
        this.formedText.textContent = words.join(' ');
        this.updateTranslation();
    }
    
    getWordSuggestions(word) {
        // Implement your word suggestion logic here
        // This is a placeholder that returns empty array
        return [];
    }
}

// Text to Sign Integration
class TextToSignApp {
    constructor() {
        this.textInput = document.getElementById('text-input');
        this.convertButton = document.getElementById('convert-text');
        this.animationContainer = document.getElementById('sign-animation-container');
        this.playButton = document.getElementById('play-animation');
        this.pauseButton = document.getElementById('pause-animation');
        this.speedControl = document.getElementById('speed-control');
        
        this.currentAnimation = null;
        this.isPlaying = false;
        
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        this.convertButton.addEventListener('click', () => this.convertTextToSign());
        this.playButton.addEventListener('click', () => this.playAnimation());
        this.pauseButton.addEventListener('click', () => this.pauseAnimation());
        this.speedControl.addEventListener('input', () => this.updateSpeed());
    }
    
    async convertTextToSign() {
        const text = this.textInput.value.trim();
        if (!text) return;
        
        this.convertButton.textContent = 'Converting...';
        this.convertButton.disabled = true;
        
        try {
            // Implement your text to sign conversion logic here
            // This is a placeholder
            await this.generateSignAnimation(text);
            
        } catch (err) {
            console.error('Conversion error:', err);
            alert('Error converting text to sign language');
        } finally {
            this.convertButton.textContent = 'Convert to Signs';
            this.convertButton.disabled = false;
        }
    }
    
    async generateSignAnimation(text) {
        // Implement your animation generation logic here
        // This is a placeholder
        this.animationContainer.innerHTML = '<p>Animation placeholder for: ' + text + '</p>';
    }
    
    playAnimation() {
        if (this.currentAnimation) {
            this.isPlaying = true;
            // Implement play logic
        }
    }
    
    pauseAnimation() {
        if (this.currentAnimation) {
            this.isPlaying = false;
            // Implement pause logic
        }
    }
    
    updateSpeed() {
        const speed = parseFloat(this.speedControl.value);
        if (this.currentAnimation) {
            // Implement speed update logic
        }
    }
}

// Initialize applications when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const signToTextApp = new SignToTextApp();
    const textToSignApp = new TextToSignApp();
});

// Handle DTI2 Launch
document.querySelectorAll('a[href="#try-sign-to-text"]').forEach(link => {
    link.addEventListener('click', async (e) => {
        e.preventDefault();
        
        try {
            const response = await fetch('/launch-dti2');
            const data = await response.json();
            
            if (data.status === 'success') {
                // Show success message
                const message = document.createElement('div');
                message.className = 'launch-message success';
                message.innerHTML = `
                    <i class="fas fa-check-circle"></i>
                    <p>DTI2 application launched successfully!</p>
                `;
                document.body.appendChild(message);
                
                // Remove message after 3 seconds
                setTimeout(() => {
                    message.remove();
                }, 3000);
            } else {
                throw new Error(data.message);
            }
        } catch (err) {
            // Show error message
            const message = document.createElement('div');
            message.className = 'launch-message error';
            message.innerHTML = `
                <i class="fas fa-exclamation-circle"></i>
                <p>Error launching DTI2: ${err.message}</p>
            `;
            document.body.appendChild(message);
            
            // Remove message after 5 seconds
            setTimeout(() => {
                message.remove();
            }, 5000);
        }
    });
});

// Add styles for launch messages
const launchStyles = document.createElement('style');
launchStyles.textContent = `
    .launch-message {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem;
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 1rem;
        animation: slideIn 0.3s ease-out;
        z-index: 9999;
    }
    
    .launch-message.success {
        background: #4CAF50;
        color: white;
    }
    
    .launch-message.error {
        background: #f44336;
        color: white;
    }
    
    .launch-message i {
        font-size: 1.5rem;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(launchStyles); 