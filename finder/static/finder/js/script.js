// This script handles the interactivity and animations for the file upload form

// Add animations and interactivity
document.addEventListener('DOMContentLoaded', function() {
    // File input animation and display filename
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        // Hide the actual file input
        input.style.display = 'none';
        
        input.addEventListener('change', function() {
            const fileNameDisplay = this.closest('.file-input-container').querySelector('.file-name');
            if (this.files.length > 0) {
                fileNameDisplay.textContent = this.files[0].name;
                fileNameDisplay.style.color = "var('--primary-color');"
            } else {
                fileNameDisplay.textContent = 'No file selected';
                fileNameDisplay.style.color = "var('--secondary-text');"
            }
        });
    });

    // Form submission animation
    const form = document.getElementById('upload-form');
    const submitButton = document.getElementById('submit-button');
    
    form.addEventListener('submit', function() {
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
        submitButton.disabled = true;
        
        // Add loading state
        document.body.style.cursor = 'wait';
    });

    // Auto-dismiss success messages after 5 seconds
    const successMessages = document.querySelectorAll('.success');
    if (successMessages.length > 0) {
        setTimeout(() => {
            successMessages.forEach(msg => {
                msg.style.opacity = '0';
                msg.style.transition = 'opacity 0.5s ease';
                setTimeout(() => msg.remove(), 500);
            });
        }, 5000);
    }
});