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
            mobileMenu.classList.remove('translate-x-full');
        });

        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                mobileMenu.classList.add('translate-x-full');
            });
        }

        // Close when clicking outside
        mobileMenu.addEventListener('click', (e) => {
            if (e.target === mobileMenu) {
                mobileMenu.classList.add('translate-x-full');
            }
        });
    }
}

function initScrollEffects() {
    const header = document.querySelector('header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 10) {
                header.classList.add('shadow-md', 'backdrop-blur-md', 'bg-white/90', 'dark:bg-slate-900/90');
                header.classList.remove('bg-transparent');
            } else {
                header.classList.remove('shadow-md', 'backdrop-blur-md', 'bg-white/90', 'dark:bg-slate-900/90');
                header.classList.add('bg-transparent'); // Or whatever initial state
            }
        });
    }
}
