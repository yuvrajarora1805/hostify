// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add fade-in animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all feature cards and steps
document.querySelectorAll('.feature-card, .step, .demo-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Add typing effect to code demo (optional enhancement)
const codeElement = document.querySelector('.code-demo code');
if (codeElement) {
    const originalText = codeElement.innerHTML;
    let isTyped = false;

    const typeCode = () => {
        if (isTyped) return;
        isTyped = true;

        codeElement.innerHTML = '';
        let i = 0;
        const speed = 20;

        const type = () => {
            if (i < originalText.length) {
                codeElement.innerHTML += originalText.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        };

        // Start typing after a short delay
        setTimeout(type, 500);
    };

    // Trigger typing when code demo comes into view
    const codeObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                typeCode();
                codeObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    codeObserver.observe(document.querySelector('.code-demo'));
}

// Add parallax effect to hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    if (hero) {
        hero.style.transform = `translateY(${scrolled * 0.5}px)`;
        hero.style.opacity = 1 - (scrolled / 600);
    }
});

console.log('🚀 Hostify Demo Site Loaded!');
console.log('This site is hosted using the hostify library');
