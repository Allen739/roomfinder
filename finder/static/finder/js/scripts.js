document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const resultsContainer = document.getElementById('results-container');
    const modal = document.getElementById('room-modal');
    const modalBody = document.getElementById('modal-body');
    const closeModal = document.querySelector('.close-button');

    // Search Form Submission (AJAX)
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(searchForm);

            fetch(searchForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.text())
            .then(html => {
                resultsContainer.innerHTML = html;
            })
            .catch(error => {
                console.error('Search error:', error);
                resultsContainer.innerHTML = '<div class="card"><p class="error">An unexpected error occurred. Please try again.</p></div>';
            });
        });
    }

    // Room Details Modal
    resultsContainer.addEventListener('click', function(e) {
        const timelineRow = e.target.closest('.timeline-row');
        if (timelineRow) {
            const roomId = timelineRow.dataset.roomId;
            const day = document.getElementById('id_day').value;
            fetch(`/api/room/${roomId}/?day=${day}`)
                .then(response => response.json())
                .then(data => {
                    modalBody.innerHTML = `
                        <h2>${data.room.name}</h2>
                        <p class="room-building">${data.room.building}</p>
                        <div class="room-details">
                            <p><strong>Capacity:</strong> ${data.room.capacity} seats</p>
                            <p><strong>Amenities:</strong> ${data.room.amenities.join(', ')}</p>
                        </div>
                        <h3 class="schedule-title">Schedule for ${day}</h3>
                        <ul class="schedule-list">
                            ${data.timeline.map(block => `
                                <li class="schedule-item">
                                    <span class="schedule-time">${block.start} - ${block.end}</span>
                                    <span class="schedule-status ${block.type}">
                                        ${block.type === 'free' ? 'Free' : `Booked: ${block.course}`}
                                    </span>
                                </li>
                            `).join('')}
                        </ul>
                    `;
                    modal.classList.add('show');
                });
        }
    });

    closeModal.addEventListener('click', function() {
        modal.classList.remove('show');
    });

    window.addEventListener('click', function(e) {
        if (e.target == modal) {
            modal.classList.remove('show');
        }
    });

    // Tab Toggling
    resultsContainer.addEventListener('click', function(e) {
        const tabLink = e.target.closest('.tab-link');
        if (tabLink) {
            const tabId = tabLink.dataset.tab;
            
            // Update active tab link
            resultsContainer.querySelectorAll('.tab-link').forEach(link => link.classList.remove('active'));
            tabLink.classList.add('active');

            // Update active tab content
            resultsContainer.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            resultsContainer.querySelector(`#${tabId}`).classList.add('active');
        }
    });

    // Upload Page Functionality (Drag & Drop)
    const roomsDropZone = document.getElementById('rooms-drop-zone');
    const timetableDropZone = document.getElementById('timetable-drop-zone');

    function setupDropZone(dropZone, fileInput, fileNameDisplay) {
        if (!dropZone) return;

        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('drag-over');
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('drag-over');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                fileNameDisplay.textContent = files[0].name;
                dropZone.classList.add('file-selected'); // Add a class for visual feedback
            }
        });

        fileInput.addEventListener('change', () => {
            if (fileInput.files.length > 0) {
                fileNameDisplay.textContent = fileInput.files[0].name;
                dropZone.classList.add('file-selected'); // Add a class for visual feedback
            } else {
                fileNameDisplay.textContent = 'No file selected';
                dropZone.classList.remove('file-selected'); // Remove class if no file
            }
        });
    }

    setupDropZone(
        roomsDropZone,
        document.getElementById('id_rooms_file'),
        document.getElementById('rooms-file-name')
    );

    setupDropZone(
        timetableDropZone,
        document.getElementById('id_timetable_file'),
        document.getElementById('timetable-file-name')
    );

    // Handle form submission for upload
    const uploadForm = document.getElementById('upload-form');
    const submitButton = document.getElementById('submit-button');

    if (uploadForm && submitButton) {
        uploadForm.addEventListener('submit', function(e) {
            const roomsFile = document.getElementById('id_rooms_file').files.length > 0;
            const timetableFile = document.getElementById('id_timetable_file').files.length > 0;

            if (!roomsFile && !timetableFile) {
                e.preventDefault();
                alert('Please select at least one file to upload.'); // Replace with a nicer toast later
                return;
            }

            submitButton.disabled = true;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
        });
    }
});