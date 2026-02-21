// Main JavaScript for Data Recovery Services Website

document.addEventListener('DOMContentLoaded', () => {
    initDarkMode();
    initMobileMenu();
    initScrollEffects();
});

function initDarkMode() {
    const toggleBtns = document.querySelectorAll('.theme-toggle');
    const html = document.documentElement;

    // Check local storage or system preference
    if (localStorage.getItem('theme') === 'dark' ||
        (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        html.classList.add('dark');
    } else {
        html.classList.remove('dark');
        // Default is light, strict check
        if (localStorage.getItem('theme') === 'light') html.classList.remove('dark');
    }

    toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            html.classList.toggle('dark');
            if (html.classList.contains('dark')) {
                localStorage.setItem('theme', 'dark');
            } else {
                localStorage.setItem('theme', 'light');
            }
        });
    });
}

function initMobileMenu() {
    const menuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const closeBtn = document.getElementById('close-menu-btn');

    if (menuBtn && mobileMenu) {
        menuBtn.addEventListener('click', () => {
            mobileMenu.classList.remove('translate-x-full', '-translate-x-full');
        });

        const closeMenu = () => {
            if (mobileMenu.classList.contains('md:static')) {
                // Dashboard sidebar
                mobileMenu.classList.add('-translate-x-full');
            } else {
                // Site-wide mobile menu
                mobileMenu.classList.add('translate-x-full');
            }
        };

        if (closeBtn) {
            closeBtn.addEventListener('click', closeMenu);
        }

        // Close when clicking outside (for site-wide menu with overlay)
        mobileMenu.addEventListener('click', (e) => {
            if (e.target === mobileMenu) {
                closeMenu();
            }
        });
    }
}

function initScrollEffects() {
    const header = document.querySelector('header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 20) {
                header.classList.add('shadow-md');
                header.classList.remove('shadow-sm');
                // Optional: slight opacity change if desired, but keeping it solid for visibility
                header.classList.add('bg-white/95', 'dark:bg-dark-bg/95');
            } else {
                header.classList.remove('shadow-md');
                header.classList.add('shadow-sm');
            }
        });
    }
}
