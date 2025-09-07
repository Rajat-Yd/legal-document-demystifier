// Legal Document Demystifier - Frontend Interactions

document.addEventListener('DOMContentLoaded', function() {
    
    // Action card selection
    const actionCards = document.querySelectorAll('.action-card');
    const actionRadios = document.querySelectorAll('input[name="action"]');
    const questionInput = document.getElementById('questionInput');
    const uploadForm = document.getElementById('uploadForm');
    const submitBtn = document.getElementById('submitBtn');
    const submitText = document.getElementById('submitText');
    const loadingSpinner = document.getElementById('loadingSpinner');

    // Handle action card clicks
    actionCards.forEach(card => {
        card.addEventListener('click', function() {
            const action = this.dataset.action;
            const radio = document.getElementById(action);
            
            // Clear previous selections
            actionCards.forEach(c => c.classList.remove('selected'));
            
            // Select current card
            this.classList.add('selected');
            radio.checked = true;
            
            // Show/hide question input
            if (action === 'question') {
                questionInput.style.display = 'block';
                questionInput.querySelector('textarea').required = true;
                questionInput.scrollIntoView({ behavior: 'smooth' });
            } else {
                questionInput.style.display = 'none';
                questionInput.querySelector('textarea').required = false;
            }
            
            // Update submit button text
            updateSubmitButtonText(action);
        });
    });

    // Handle radio button changes (for keyboard navigation)
    actionRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.checked) {
                const card = document.querySelector(`[data-action="${this.value}"]`);
                if (card) {
                    card.click();
                }
            }
        });
    });

    // Form submission handling
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            const fileInput = document.getElementById('file');
            const selectedAction = document.querySelector('input[name="action"]:checked');
            
            // Validate file selection
            if (!fileInput.files.length) {
                e.preventDefault();
                showAlert('Please select a file to upload.', 'error');
                return;
            }
            
            // Validate action selection
            if (!selectedAction) {
                e.preventDefault();
                showAlert('Please select an action.', 'error');
                return;
            }
            
            // Validate question if Q&A is selected
            if (selectedAction.value === 'question') {
                const questionText = document.getElementById('question').value.trim();
                if (!questionText) {
                    e.preventDefault();
                    showAlert('Please enter a question.', 'error');
                    return;
                }
            }
            
            // Validate file type
            const fileName = fileInput.files[0].name.toLowerCase();
            if (!fileName.endsWith('.pdf') && !fileName.endsWith('.txt')) {
                e.preventDefault();
                showAlert('Please select a PDF or TXT file.', 'error');
                return;
            }
            
            // Validate file size (16MB = 16 * 1024 * 1024 bytes)
            if (fileInput.files[0].size > 16 * 1024 * 1024) {
                e.preventDefault();
                showAlert('File size must be less than 16MB.', 'error');
                return;
            }
            
            // Show loading state
            showLoadingState();
        });
    }

    // Question form handling (for follow-up questions)
    const questionForm = document.getElementById('questionForm');
    if (questionForm) {
        questionForm.addEventListener('submit', function() {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                submitButton.disabled = true;
            }
        });
    }

    // Utility functions
    function updateSubmitButtonText(action) {
        const actionTexts = {
            'simplify': 'Simplify Document',
            'summarize': 'Summarize Document',
            'question': 'Get Answer'
        };
        
        if (submitText) {
            submitText.textContent = actionTexts[action] || 'Process Document';
        }
    }

    function showLoadingState() {
        if (submitBtn && submitText && loadingSpinner) {
            submitBtn.disabled = true;
            submitBtn.classList.add('loading');
            submitText.textContent = 'Processing...';
            loadingSpinner.classList.remove('d-none');
        }
    }

    function showAlert(message, type = 'info') {
        // Create alert element
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'check-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insert alert at the top of the container
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(alertDiv, container.firstChild);
            alertDiv.scrollIntoView({ behavior: 'smooth' });
        }
    }

    // File input change handler
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const fileName = this.files[0]?.name;
            if (fileName) {
                // Update file input label or show file name
                const fileInfo = this.nextElementSibling;
                if (fileInfo && fileInfo.classList.contains('form-text')) {
                    fileInfo.innerHTML = `
                        <i class="fas fa-check-circle text-success me-1"></i>
                        Selected: ${fileName}
                    `;
                }
            }
        });
    }

    // Auto-dismiss alerts after 5 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            if (alert.querySelector('.btn-close')) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        });
    }, 5000);

    // Smooth scrolling for anchor links
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

    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});

// Global utility functions
window.LegalDocApp = {
    copyToClipboard: function(text) {
        navigator.clipboard.writeText(text).then(() => {
            this.showToast('Copied to clipboard!', 'success');
        }).catch(() => {
            this.showToast('Failed to copy to clipboard', 'error');
        });
    },
    
    showToast: function(message, type = 'info') {
        // Simple toast implementation
        const toast = document.createElement('div');
        toast.className = `alert alert-${type === 'error' ? 'danger' : 'success'} position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'check-circle'} me-2"></i>
            ${message}
        `;
        
        document.body.appendChild(toast);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }
};
