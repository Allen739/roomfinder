// Enhanced scripts.js - Handles both search and upload functionality
document.addEventListener('DOMContentLoaded', function() {
    
    // Toast notification utility
    function showToast(message, duration = 3000) {
        const toast = document.getElementById('toast');
        if (toast) {
            toast.textContent = message;
            toast.classList.add('show');
            
            setTimeout(function() {
                toast.classList.remove('show');
            }, duration);
        }
    }
    
    // Search form functionality
    const searchBtn = document.getElementById('searchBtn');
    if (searchBtn) {
        const searchForm = searchBtn.closest('form');
        
        searchBtn.addEventListener('click', function(e) {
            // Add loading state
            searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin search-btn-icon"></i> Searching...';
            searchBtn.disabled = true;
            
            // Show toast notification
            showToast('🔍 Searching for available rooms...');
        });
        
        // Reset button state on form validation errors
        if (searchForm) {
            searchForm.addEventListener('submit', function() {
                setTimeout(() => {
                    if (document.querySelector('.error')) {
                        searchBtn.innerHTML = '<i class="fas fa-search search-btn-icon"></i> Find Rooms';
                        searchBtn.disabled = false;
                    }
                }, 100);
            });
        }
    }
    
    // Room item interactions
    const roomItems = document.querySelectorAll('.room-item');
    roomItems.forEach(item => {
        item.addEventListener('click', function() {
            // Add selection effect
            this.style.backgroundColor = 'var(--primary-light)';
            this.style.transform = 'scale(0.98)';
            
            // Show feedback
            const roomName = this.querySelector('.room-name').textContent;
            showToast(`✓ Selected ${roomName}! Room details noted.`);
            
            // Reset after animation
            setTimeout(() => {
                this.style.backgroundColor = '';
                this.style.transform = '';
            }, 1000);
        });
        
        // Add hover effects
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
    
    // File upload functionality
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const container = this.closest('.file-input-container');
            const fileNameDisplay = container.querySelector('.file-name');
            const label = container.querySelector('.file-input-label');
            
            if (this.files.length > 0) {
                const fileName = this.files[0].name;
                const fileSize = (this.files[0].size / 1024 / 1024).toFixed(2);
                fileNameDisplay.textContent = `${fileName} (${fileSize} MB)`;
                fileNameDisplay.style.color = 'var(--primary)';
                fileNameDisplay.style.fontWeight = '500';
                
                // Add success styling to label
                label.style.borderColor = 'var(--secondary)';
                label.style.backgroundColor = 'var(--secondary-light)';
                
                // Show toast
                showToast(`📁 File selected: ${fileName}`);
            } else {
                fileNameDisplay.textContent = 'No file selected';
                fileNameDisplay.style.color = 'var(--gray)';
                fileNameDisplay.style.fontWeight = 'normal';
                
                // Reset label styling
                label.style.borderColor = 'var(--border)';
                label.style.backgroundColor = 'var(--gray-light)';
            }
        });
    });
    
    // Upload form submission
    const uploadForm = document.getElementById('upload-form');
    const submitButton = document.getElementById('submit-button');
    
    if (uploadForm && submitButton) {
        uploadForm.addEventListener('submit', function(e) {
            // Check if at least one file is selected
            const hasFiles = Array.from(fileInputs).some(input => input.files.length > 0);
            
            if (!hasFiles) {
                e.preventDefault();
                showToast('⚠️ Please select at least one file to upload', 4000);
                return;
            }
            
            // Add loading state
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
            submitButton.disabled = true;
            uploadForm.classList.add('loading');
            
            // Show progress toast
            showToast('📤 Upload in progress... Please wait', 10000);
            
            // Add loading cursor
            document.body.style.cursor = 'wait';
        });
    }
    
    // Auto-dismiss success messages
    const successMessages = document.querySelectorAll('.success-message');
    if (successMessages.length > 0) {
        setTimeout(() => {
            successMessages.forEach(msg => {
                msg.style.opacity = '0';
                msg.style.transition = 'opacity 0.5s ease';
                setTimeout(() => {
                    if (msg.parentNode) {
                        msg.remove();
                    }
                }, 500);
            });
        }, 5000);
    }
    
    // Navigation enhancements
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Add loading state for navigation
            this.style.opacity = '0.7';
            showToast('🔄 Navigating...');
        });
    });
    
    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, select');
        
        inputs.forEach(input => {
            // Real-time validation feedback
            input.addEventListener('blur', function() {
                if (this.checkValidity()) {
                    this.style.borderColor = 'var(--secondary)';
                } else {
                    this.style.borderColor = 'var(--danger)';
                }
            });
            
            input.addEventListener('focus', function() {
                this.style.borderColor = 'var(--primary)';
            });
        });
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit forms
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const activeForm = document.querySelector('form');
            if (activeForm) {
                const submitBtn = activeForm.querySelector('button[type="submit"]');
                if (submitBtn && !submitBtn.disabled) {
                    submitBtn.click();
                }
            }
        }
        
        // Escape to clear selections
        if (e.key === 'Escape') {
            roomItems.forEach(item => {
                item.style.backgroundColor = '';
                item.style.transform = '';
            });
        }
    });
    
    // Performance optimization - lazy load animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe modules for animation
    const modules = document.querySelectorAll('.module');
    modules.forEach(module => {
        module.style.opacity = '0';
        module.style.transform = 'translateY(20px)';
        module.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(module);
    });
    
});

// Utility functions for external use
window.RoomFinder = {
    showToast: function(message, duration = 3000) {
        const toast = document.getElementById('toast');
        if (toast) {
            toast.textContent = message;
            toast.classList.add('show');
            
            setTimeout(function() {
                toast.classList.remove('show');
            }, duration);
        }
    },
    
    resetLoadingStates: function() {
        document.body.style.cursor = '';
        const loadingElements = document.querySelectorAll('.loading');
        loadingElements.forEach(el => el.classList.remove('loading'));
        
        const disabledButtons = document.querySelectorAll('button[disabled]');
        disabledButtons.forEach(btn => {
            btn.disabled = false;
            if (btn.id === 'searchBtn') {
                btn.innerHTML = '<i class="fas fa-search search-btn-icon"></i> Find Rooms';
            } else if (btn.id === 'submit-button') {
                btn.innerHTML = '<i class="fas fa-cloud-upload-alt"></i> Upload Files';
            }
        });
    }
};