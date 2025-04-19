// Script.js

       // Add click animation to search button
       const searchBtn = document.getElementById('searchBtn');
       if (searchBtn) {
           searchBtn.addEventListener('click', function() {
               // Show toast notification when form is submitted
               const toast = document.getElementById('toast');
               toast.classList.add('show');
               
               // Hide toast after 3 seconds
               setTimeout(function() {
                   toast.classList.remove('show');
               }, 3000);
           });
       }
       
       // Add hover animation to room items
       const roomItems = document.querySelectorAll('.room-item');
       roomItems.forEach(item => {
           item.addEventListener('click', function() {
               // Add selection effect
               this.style.backgroundColor = 'var(--primary-light)';
               this.style.transform = 'scale(0.98)';
               
               // Show quick feedback
               const toast = document.getElementById('toast');
               toast.textContent = '✓ Room selected! Click again to book';
               toast.classList.add('show');
               
               // Reset after animation
               setTimeout(() => {
                   this.style.backgroundColor = '';
                   this.style.transform = '';
                   toast.classList.remove('show');
               }, 1000);
           });
       });