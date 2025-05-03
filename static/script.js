document.addEventListener('DOMContentLoaded', () => {
    // Initialize DOM elements
    const menuBtn = document.querySelector('.menu-btn');
    const navLinks = document.querySelector('.nav-links');
    const carousel = document.querySelector('.carousel');
    const carouselTrack = document.querySelector('.carousel-track');
    const carouselSlides = document.querySelectorAll('.carousel-slide');
    const prevBtn = document.querySelector('.carousel-btn.prev');
    const nextBtn = document.querySelector('.carousel-btn.next');
    const dotsContainer = document.querySelector('.carousel-dots');

    // Initialize variables
    let currentSlide = 0;
    const slideWidth = carouselSlides[0].offsetWidth;

    // Mobile menu functionality
    menuBtn.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        menuBtn.classList.toggle('active');
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!menuBtn.contains(e.target) && !navLinks.contains(e.target)) {
            navLinks.classList.remove('active');
            menuBtn.classList.remove('active');
        }
    });

    // Close menu when clicking a link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            menuBtn.classList.remove('active');
        });
    });
    const carousel = document.querySelector('.carousel');
    const carouselTrack = document.querySelector('.carousel-track');
    const carouselSlides = document.querySelectorAll('.carousel-slide');
    const prevBtn = document.querySelector('.carousel-btn.prev');
    const nextBtn = document.querySelector('.carousel-btn.next');
    const dotsContainer = document.querySelector('.carousel-dots');

    let currentSlide = 0;
    const slideWidth = carouselSlides[0].offsetWidth;

    // Create dots
    carouselSlides.forEach((_, index) => {
        const dot = document.createElement('div');
        dot.className = `carousel-dot ${index === 0 ? 'active' : ''}`;
        dot.addEventListener('click', () => goToSlide(index));
        dotsContainer.appendChild(dot);
    });

    // Update dots
    function updateDots() {
        const dots = document.querySelectorAll('.carousel-dot');
        dots.forEach((dot, index) => {
            dot.className = `carousel-dot ${index === currentSlide ? 'active' : ''}`;
        });
    }

    // Move to specific slide
    function goToSlide(slideIndex) {
        currentSlide = slideIndex;
        carouselTrack.style.transform = `translateX(-${slideWidth * currentSlide}px)`;
        updateDots();
    }

    // Previous slide
    function prevSlide() {
        currentSlide = (currentSlide - 1 + carouselSlides.length) % carouselSlides.length;
        goToSlide(currentSlide);
    }

    // Next slide
    function nextSlide() {
        currentSlide = (currentSlide + 1) % carouselSlides.length;
        goToSlide(currentSlide);
    }

    // Add event listeners
    prevBtn.addEventListener('click', prevSlide);
    nextBtn.addEventListener('click', nextSlide);

    // Auto-rotate every 5 seconds
    let autoRotate = setInterval(nextSlide, 5000);

    // Pause rotation on hover
    carousel.addEventListener('mouseenter', () => {
        clearInterval(autoRotate);
    });

    carousel.addEventListener('mouseleave', () => {
        autoRotate = setInterval(nextSlide, 5000);
    });
    // Mobile menu functionality
    const menuBtn = document.querySelector('.menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (menuBtn && navLinks) {
        menuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!menuBtn.contains(e.target) && !navLinks.contains(e.target)) {
                navLinks.classList.remove('active');
            }
        });
    }

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
                // Close mobile menu if open
                if (navLinks) {
                    navLinks.classList.remove('active');
                }
            }
        });
    });

    // Form submission handling
    const contactForm = document.getElementById('contact-form');
    const mailingListForm = document.getElementById('mailing-list-form');

    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(contactForm);
            const data = {
                name: formData.get('name'),
                email: formData.get('email'),
                message: formData.get('message')
            };

            try {
                const response = await fetch('/send_email', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                
                if (result.success) {
                    alert('Message sent successfully!');
                    contactForm.reset();
                } else {
                    alert('Error sending message: ' + result.message);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error sending message. Please try again later.');
            }
        });
    }

    if (mailingListForm) {
        mailingListForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(mailingListForm);
            const email = formData.get('email');

            try {
                console.log('Submitting subscription with email:', email);
                const response = await fetch('/api/subscribe', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email })
                });
                console.log('Server response status:', response.status);

                const result = await response.json();
                console.log('Server response:', result);
                
                if (response.status === 200) {
                    alert('Successfully subscribed!');
                    mailingListForm.reset();
                } else {
                    alert('Error subscribing: ' + (result.error || 'Unknown error'));
                }
            } catch (error) {
                console.error('Error during subscription:', error);
                alert('Error subscribing. Please try again later.');
            }
        });
    }

    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, observerOptions);

    // Observe sections for scroll animations
    document.querySelectorAll('section').forEach(section => {
        observer.observe(section);
    });

    // Add scroll event listener for navbar background change
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        } else {
            navbar.style.background = 'var(--white)';
        }
    });
});
