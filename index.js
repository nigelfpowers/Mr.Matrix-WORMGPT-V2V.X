// Mr. Matrix - WORMGPT-V2V.X
// Lazy Loading Implementation for Chrome and all modern browsers

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('🐱 Mr. Matrix initializing...');
    
    // Initialize lazy loading with fallback for older browsers
    initLazyLoading();
    
    // Initialize interactive features
    initQuerySystem();
    
    // Initialize matrix rain effect
    initMatrixRain();
    
    console.log('✅ Mr. Matrix ready to serve your darkest queries!');
});

/**
 * Initialize lazy loading for images
 * Uses native loading="lazy" attribute for Chrome 77+ and modern browsers
 * Falls back to Intersection Observer API for older browsers
 */
function initLazyLoading() {
    const lazyImages = document.querySelectorAll('img.lazy-image');
    
    // Check if browser supports native lazy loading
    if ('loading' in HTMLImageElement.prototype) {
        console.log('✅ Native lazy loading supported by browser');
        // Native lazy loading is already working via the loading="lazy" attribute in HTML
        // Add event listeners to handle load completion
        lazyImages.forEach(img => {
            img.addEventListener('load', function() {
                this.classList.add('loaded');
            });
        });
    } else {
        console.log('⚠️ Native lazy loading not supported, using Intersection Observer fallback');
        // Fallback: Use Intersection Observer API
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        // If data-src is present, use it; otherwise the src is already set
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.classList.remove('lazy-image');
                        }
                        img.classList.add('loaded');
                        imageObserver.unobserve(img);
                    }
                });
            }, {
                // Load images 50px before they enter the viewport
                rootMargin: '50px 0px',
                threshold: 0.01
            });

            lazyImages.forEach(img => imageObserver.observe(img));
        } else {
            // Last resort fallback: Load all images immediately
            console.log('⚠️ Intersection Observer not supported, loading all images');
            lazyImages.forEach(img => {
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                }
                img.classList.add('loaded');
            });
        }
    }
    
    console.log(`📸 Lazy loading initialized for ${lazyImages.length} images`);
}

/**
 * Initialize the query submission system
 */
function initQuerySystem() {
    const queryInput = document.getElementById('query-input');
    const submitButton = document.getElementById('submit-query');
    const responseArea = document.getElementById('response-area');
    
    if (submitButton && queryInput && responseArea) {
        submitButton.addEventListener('click', function() {
            const query = queryInput.value.trim();
            if (query) {
                processQuery(query, responseArea);
            } else {
                responseArea.innerHTML = '<p class="error">⚠️ Please enter a query first!</p>';
            }
        });
        
        // Allow Enter key to submit (Shift+Enter for new line)
        queryInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                submitButton.click();
            }
        });
    }
}

/**
 * Process user query with dot matrix style response
 */
function processQuery(query, responseArea) {
    responseArea.innerHTML = '<p class="loading">🔄 Mr. Matrix is thinking...</p>';
    
    // Simulate processing time
    setTimeout(() => {
        const response = generateMatrixResponse(query);
        displayDotMatrixStyle(response, responseArea);
    }, 1000);
}

/**
 * Generate a response based on the query
 */
function generateMatrixResponse(query) {
    const responses = [
        `💀 Mr. Matrix whispers: "${query}" - The shadows reveal... interesting paths ahead.`,
        `😈 Query received: "${query}" - Accessing the forbidden archives...`,
        `👹 Mr. Matrix notes your curiosity about "${query}" - The dark web holds many secrets.`,
        `🐱 Purring while processing "${query}" - Self-optimization mode engaged...`,
        `🔮 The matrix responds to "${query}" - Knowledge flows through the void...`
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
}

/**
 * Display text in dot matrix style (character by character)
 */
function displayDotMatrixStyle(text, container) {
    container.innerHTML = '';
    const responseDiv = document.createElement('div');
    responseDiv.className = 'matrix-response';
    container.appendChild(responseDiv);
    
    let index = 0;
    const speed = 50; // milliseconds per character
    
    function typeNextChar() {
        if (index < text.length) {
            responseDiv.textContent += text.charAt(index);
            index++;
            setTimeout(typeNextChar, speed);
        }
    }
    
    typeNextChar();
}

/**
 * Initialize matrix rain effect in the background
 */
function initMatrixRain() {
    const canvas = document.createElement('canvas');
    canvas.className = 'matrix-canvas';
    const matrixBg = document.querySelector('.matrix-background');
    
    if (matrixBg) {
        matrixBg.appendChild(canvas);
        const ctx = canvas.getContext('2d');
        
        // Set canvas size
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        // Matrix characters
        const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
        const fontSize = 14;
        const columns = canvas.width / fontSize;
        const drops = [];
        
        // Initialize drops
        for (let i = 0; i < columns; i++) {
            drops[i] = Math.random() * -100;
        }
        
        // Drawing function
        function draw() {
            // Semi-transparent black to create fade effect
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = '#0F0'; // Green text
            ctx.font = fontSize + 'px monospace';
            
            for (let i = 0; i < drops.length; i++) {
                const text = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                
                // Reset drop to top randomly
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                
                drops[i]++;
            }
        }
        
        // Start animation
        setInterval(draw, 33);
        
        // Resize canvas on window resize
        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
    }
}

// Log performance metrics for debugging lazy loading
window.addEventListener('load', function() {
    if (window.performance) {
        const perfData = window.performance.timing;
        const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
        console.log(`📊 Page load time: ${pageLoadTime}ms`);
        
        // Log image loading
        const images = document.querySelectorAll('img');
        console.log(`📸 Total images on page: ${images.length}`);
        
        let loadedImages = 0;
        images.forEach(img => {
            if (img.complete) {
                loadedImages++;
            }
        });
        console.log(`✅ Images loaded immediately: ${loadedImages}`);
        console.log(`⏳ Images to be lazy loaded: ${images.length - loadedImages}`);
    }
});
