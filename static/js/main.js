// Main JavaScript file for Flask App

document.addEventListener('DOMContentLoaded', function() {
    console.log('Flask App loaded successfully!');
    
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (alert.classList.contains('show')) {
                alert.classList.remove('show');
                setTimeout(function() {
                    alert.remove();
                }, 150);
            }
        }, 5000);
    });
});

// Function to load API data
async function loadApiData() {
    const apiDataDiv = document.getElementById('api-data');
    const apiContentPre = document.getElementById('api-content');
    const button = event.target;
    
    // Show loading state
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Loading...';
    
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        
        // Display the data
        apiContentPre.textContent = JSON.stringify(data, null, 2);
        apiDataDiv.style.display = 'block';
        apiDataDiv.classList.add('fade-in');
        
        // Update button
        button.innerHTML = 'Data Loaded!';
        button.classList.remove('btn-secondary');
        button.classList.add('btn-success');
        
        // Reset button after 3 seconds
        setTimeout(() => {
            button.innerHTML = 'Load API Data';
            button.classList.remove('btn-success');
            button.classList.add('btn-secondary');
            button.disabled = false;
        }, 3000);
        
    } catch (error) {
        console.error('Error loading API data:', error);
        
        // Show error state
        apiContentPre.textContent = 'Error loading data: ' + error.message;
        apiDataDiv.style.display = 'block';
        apiDataDiv.classList.remove('alert-info');
        apiDataDiv.classList.add('alert-danger');
        
        // Reset button
        button.innerHTML = 'Try Again';
        button.classList.remove('btn-secondary');
        button.classList.add('btn-danger');
        button.disabled = false;
    }
}

// Form validation for contact form
function validateContactForm() {
    const name = document.getElementById('name');
    const email = document.getElementById('email');
    const message = document.getElementById('message');
    
    let isValid = true;
    
    // Reset previous validation states
    [name, email, message].forEach(field => {
        field.classList.remove('is-invalid');
    });
    
    // Validate name
    if (name && name.value.trim().length < 2) {
        name.classList.add('is-invalid');
        isValid = false;
    }
    
    // Validate email
    if (email && !isValidEmail(email.value)) {
        email.classList.add('is-invalid');
        isValid = false;
    }
    
    // Validate message
    if (message && message.value.trim().length < 10) {
        message.classList.add('is-invalid');
        isValid = false;
    }
    
    return isValid;
}

// Email validation helper
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Add smooth scrolling to anchor links
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

// Add form validation to contact form if it exists
const contactForm = document.querySelector('form[method="POST"]');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        if (!validateContactForm()) {
            e.preventDefault();
            
            // Show validation message
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-danger alert-dismissible fade show';
            alertDiv.innerHTML = `
                <strong>Please fix the following errors:</strong>
                <ul class="mb-0 mt-2">
                    <li>Name must be at least 2 characters long</li>
                    <li>Please enter a valid email address</li>
                    <li>Message must be at least 10 characters long</li>
                </ul>
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            // Insert alert before the form
            contactForm.parentNode.insertBefore(alertDiv, contactForm);
            
            // Scroll to the alert
            alertDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    });
}
