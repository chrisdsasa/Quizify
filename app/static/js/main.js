// PDF Quiz Generator - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Range slider value display
    const rangeSlider = document.getElementById('num_questions');
    if (rangeSlider) {
        rangeSlider.addEventListener('input', function() {
            // Update a span or other element with the current value if needed
            console.log(`Number of questions: ${this.value}`);
        });
    }

    // File upload validation
    const fileInput = document.getElementById('pdf_file');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const filePath = this.value;
            const allowedExtensions = /(\.pdf)$/i;
            
            if (!allowedExtensions.exec(filePath)) {
                alert('Please upload a PDF file only');
                this.value = '';
                return false;
            }
            
            if (this.files[0].size > 16 * 1024 * 1024) { // 16MB
                alert('File size too large. Maximum file size is 16MB.');
                this.value = '';
                return false;
            }
        });
    }

    // Quiz navigation
    const nextButtons = document.querySelectorAll('.next-question');
    if (nextButtons.length > 0) {
        nextButtons.forEach(button => {
            button.addEventListener('click', function() {
                const currentQuestion = this.closest('.question-card');
                const nextQuestion = currentQuestion.nextElementSibling;
                
                if (nextQuestion && nextQuestion.classList.contains('question-card')) {
                    currentQuestion.style.display = 'none';
                    nextQuestion.style.display = 'block';
                }
            });
        });
    }

    // Quiz form validation
    const quizForm = document.getElementById('quiz-form');
    if (quizForm) {
        quizForm.addEventListener('submit', function(event) {
            let allQuestionsAnswered = true;
            const questions = document.querySelectorAll('.question-card');
            
            questions.forEach(question => {
                const questionId = question.dataset.questionId;
                const answered = document.querySelector(`input[name="question_${questionId}"]:checked`);
                
                if (!answered) {
                    allQuestionsAnswered = false;
                }
            });
            
            if (!allQuestionsAnswered) {
                event.preventDefault();
                alert('Please answer all questions before submitting.');
            }
        });
    }

    // Copy share link to clipboard
    const copyLinkBtn = document.getElementById('copy-link');
    if (copyLinkBtn) {
        copyLinkBtn.addEventListener('click', function() {
            const shareUrl = document.getElementById('share-url');
            if (shareUrl) {
                navigator.clipboard.writeText(shareUrl.value).then(() => {
                    // Update button text temporarily
                    const originalText = this.textContent;
                    this.textContent = 'Copied!';
                    
                    setTimeout(() => {
                        this.textContent = originalText;
                    }, 2000);
                });
            }
        });
    }

    // Timer for timed quizzes
    const quizTimer = document.getElementById('quiz-timer');
    if (quizTimer) {
        const timeLimit = parseInt(quizTimer.dataset.timeLimit, 10) || 0;
        if (timeLimit > 0) {
            let timeRemaining = timeLimit * 60; // Convert minutes to seconds
            
            const timer = setInterval(function() {
                if (timeRemaining <= 0) {
                    clearInterval(timer);
                    alert('Time is up! Submitting your answers now.');
                    document.getElementById('quiz-form').submit();
                    return;
                }
                
                const minutes = Math.floor(timeRemaining / 60);
                const seconds = timeRemaining % 60;
                
                quizTimer.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
                timeRemaining--;
            }, 1000);
        }
    }

    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length > 0) {
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }
});
