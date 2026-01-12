// Theme Toggle Script for Hostify Documentation

(function () {
    'use strict';

    // Create theme toggle button
    function createThemeToggle() {
        const button = document.createElement('button');
        button.id = 'theme-toggle';
        button.textContent = 'Midnight Mode';
        button.setAttribute('aria-label', 'Toggle midnight black theme');
        document.body.appendChild(button);
        return button;
    }

    // Load saved theme preference
    function loadTheme() {
        const savedTheme = localStorage.getItem('hostify-theme');
        if (savedTheme === 'midnight') {
            document.body.classList.add('midnight-theme');
        }
    }

    // Toggle theme
    function toggleTheme() {
        document.body.classList.toggle('midnight-theme');
        const isMidnight = document.body.classList.contains('midnight-theme');
        localStorage.setItem('hostify-theme', isMidnight ? 'midnight' : 'default');
        updateButtonText(isMidnight);
    }

    // Update button text
    function updateButtonText(isMidnight) {
        const button = document.getElementById('theme-toggle');
        if (button) {
            button.textContent = isMidnight ? 'Light Mode' : 'Midnight Mode';
        }
    }

    // Initialize on page load
    function init() {
        // Load saved theme first
        loadTheme();

        // Create toggle button
        const button = createThemeToggle();
        updateButtonText(document.body.classList.contains('midnight-theme'));

        // Add click event
        button.addEventListener('click', toggleTheme);
    }

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
