// Enhanced JavaScript for Hyderabad Property Deals

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS (Animate On Scroll) if available
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true
        });
    }

    // Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navMenu = document.querySelector('nav ul');
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            this.classList.toggle('active');
            navMenu.classList.toggle('active');
            
            // Animate hamburger to X
            const bars = this.querySelectorAll('.bar');
            if (this.classList.contains('active')) {
                bars[0].style.transform = 'rotate(-45deg) translate(-5px, 6px)';
                bars[1].style.opacity = '0';
                bars[2].style.transform = 'rotate(45deg) translate(-5px, -6px)';
            } else {
                bars[0].style.transform = 'none';
                bars[1].style.opacity = '1';
                bars[2].style.transform = 'none';
            }
        });
    }

    // Scroll to Top Button
    const scrollTopBtn = document.createElement('div');
    scrollTopBtn.classList.add('scroll-top');
    scrollTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    document.body.appendChild(scrollTopBtn);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollTopBtn.classList.add('active');
        } else {
            scrollTopBtn.classList.remove('active');
        }
    });
    
    scrollTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Header Scroll Effect
    const header = document.querySelector('header');
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 50) {
            header.style.padding = '10px 0';
            header.style.boxShadow = '0 5px 20px rgba(0, 0, 0, 0.1)';
        } else {
            header.style.padding = '15px 0';
            header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        }
    });

    // Contact form submission with validation
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const phone = document.getElementById('phone').value;
            const message = document.getElementById('message').value;
            
            // Simple validation
            let isValid = true;
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            if (name.trim() === '') {
                showError('name', 'Please enter your name');
                isValid = false;
            } else {
                removeError('name');
            }
            
            if (!emailRegex.test(email)) {
                showError('email', 'Please enter a valid email address');
                isValid = false;
            } else {
                removeError('email');
            }
            
            if (message.trim() === '') {
                showError('message', 'Please enter your message');
                isValid = false;
            } else {
                removeError('message');
            }
            
            if (isValid) {
                // Show success message
                const successMessage = document.createElement('div');
                successMessage.className = 'success-message';
                successMessage.innerHTML = `
                    <div class="success-icon"><i class="fas fa-check-circle"></i></div>
                    <h3>Thank you, ${name}!</h3>
                    <p>Your message has been sent successfully. We will contact you soon.</p>
                `;
                
                contactForm.innerHTML = '';
                contactForm.appendChild(successMessage);
                
                // In a real application, you would send this data to a server
                console.log('Form submitted:', { name, email, phone, message });
            }
        });
    }
    
    // Newsletter form submission
    const newsletterForm = document.getElementById('newsletterForm');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get the email value
            const emailInput = newsletterForm.querySelector('input[type="email"]');
            const email = emailInput.value;
            
            // Simple validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            if (!emailRegex.test(email)) {
                emailInput.style.borderColor = '#e74c3c';
                return;
            } else {
                emailInput.style.borderColor = '#3498db';
            }
            
            // Show success message
            const submitBtn = newsletterForm.querySelector('.btn');
            const originalText = submitBtn.textContent;
            submitBtn.innerHTML = '<i class="fas fa-check"></i> Subscribed!';
            submitBtn.style.backgroundColor = '#2ecc71';
            
            // Reset after 3 seconds
            setTimeout(() => {
                submitBtn.textContent = originalText;
                submitBtn.style.backgroundColor = '';
                newsletterForm.reset();
            }, 3000);
            
            // In a real application, you would send this data to a server
            console.log('Newsletter subscription:', email);
        });
    }
    
    // Property detail page image gallery functionality
    const mainImage = document.getElementById('mainPropertyImage');
    const thumbnails = document.querySelectorAll('.thumbnail');
    
    if (mainImage && thumbnails.length > 0) {
        thumbnails.forEach(thumbnail => {
            thumbnail.addEventListener('click', function() {
                // Get the image inside the thumbnail
                const thumbnailImg = this.querySelector('img');
                
                // Update main image src with the clicked thumbnail src
                mainImage.src = thumbnailImg.src;
                
                // Add fade effect
                mainImage.style.opacity = '0';
                setTimeout(() => {
                    mainImage.style.opacity = '1';
                }, 100);
                
                // Remove active class from all thumbnails
                thumbnails.forEach(thumb => thumb.classList.remove('active'));
                
                // Add active class to clicked thumbnail
                this.classList.add('active');
            });
        });
    }
    
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('header nav a, .hero a.btn');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Check if the link is an anchor link
            if (this.getAttribute('href').startsWith('#')) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    // Close mobile menu if open
                    if (navMenu && navMenu.classList.contains('active')) {
                        navMenu.classList.remove('active');
                        if (mobileMenuBtn) {
                            mobileMenuBtn.classList.remove('active');
                            const bars = mobileMenuBtn.querySelectorAll('.bar');
                            bars[0].style.transform = 'none';
                            bars[1].style.opacity = '1';
                            bars[2].style.transform = 'none';
                        }
                    }
                    
                    // Scroll to the target element
                    const headerHeight = document.querySelector('header').offsetHeight;
                    const targetPosition = targetElement.offsetTop - headerHeight;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
    
    // Contact agent form in property detail pages
    const contactAgentForm = document.getElementById('contactAgentForm');
    if (contactAgentForm) {
        contactAgentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const name = document.getElementById('agentContactName').value;
            const email = document.getElementById('agentContactEmail').value;
            const phone = document.getElementById('agentContactPhone').value;
            const message = document.getElementById('agentContactMessage').value;
            
            // Simple validation
            let isValid = true;
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            if (name.trim() === '') {
                showError('agentContactName', 'Please enter your name');
                isValid = false;
            } else {
                removeError('agentContactName');
            }
            
            if (!emailRegex.test(email)) {
                showError('agentContactEmail', 'Please enter a valid email address');
                isValid = false;
            } else {
                removeError('agentContactEmail');
            }
            
            if (message.trim() === '') {
                showError('agentContactMessage', 'Please enter your message');
                isValid = false;
            } else {
                removeError('agentContactMessage');
            }
            
            if (isValid) {
                // Show success message
                const successMessage = document.createElement('div');
                successMessage.className = 'success-message';
                successMessage.innerHTML = `
                    <div class="success-icon"><i class="fas fa-check-circle"></i></div>
                    <h3>Thank you, ${name}!</h3>
                    <p>Your message has been sent to the agent. They will contact you soon.</p>
                `;
                
                contactAgentForm.innerHTML = '';
                contactAgentForm.appendChild(successMessage);
                
                // In a real application, you would send this data to a server
                console.log('Agent contact form submitted:', { name, email, phone, message });
            }
        });
    }
    
    // Add active class to current navigation item
    const currentLocation = window.location.pathname;
    const navItems = document.querySelectorAll('nav ul li a');
    
    navItems.forEach(item => {
        if (item.getAttribute('href') === currentLocation || 
            item.getAttribute('href') === currentLocation.substring(currentLocation.lastIndexOf('/') + 1) ||
            (currentLocation.includes('property') && item.getAttribute('href') === '#properties')) {
            item.classList.add('active');
        }
    });
    
    // Property filtering functionality (if filter buttons exist)
    const filterBtns = document.querySelectorAll('.property-filter button');
    const propertyCards = document.querySelectorAll('.property-card');
    
    if (filterBtns.length > 0 && propertyCards.length > 0) {
        filterBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                // Remove active class from all buttons
                filterBtns.forEach(b => b.classList.remove('active'));
                
                // Add active class to clicked button
                this.classList.add('active');
                
                const filterValue = this.getAttribute('data-filter');
                
                // Show/hide property cards based on filter
                propertyCards.forEach(card => {
                    if (filterValue === 'all') {
                        card.style.display = 'block';
                    } else {
                        if (card.classList.contains(filterValue)) {
                            card.style.display = 'block';
                        } else {
                            card.style.display = 'none';
                        }
                    }
                });
            });
        });
    }
    
    // Helper functions for form validation
    function showError(inputId, message) {
        const input = document.getElementById(inputId);
        input.style.borderColor = '#e74c3c';
        
        // Remove any existing error message
        const existingError = input.parentElement.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        // Create and append error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        input.parentElement.appendChild(errorDiv);
    }
    
    function removeError(inputId) {
        const input = document.getElementById(inputId);
        input.style.borderColor = '';
        
        // Remove any existing error message
        const existingError = input.parentElement.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
    }
    
    // Add CSS for dynamic elements
    const style = document.createElement('style');
    style.textContent = `
        .error-message {
            color: #e74c3c;
            font-size: 0.85rem;
            margin-top: 5px;
        }
        
        .success-message {
            text-align: center;
            padding: 30px;
        }
        
        .success-icon {
            font-size: 3rem;
            color: #2ecc71;
            margin-bottom: 20px;
        }
        
        .success-message h3 {
            margin-bottom: 10px;
            color: #2c3e50;
        }
        
        .success-message p {
            color: #7f8c8d;
        }
    `;
    document.head.appendChild(style);
});