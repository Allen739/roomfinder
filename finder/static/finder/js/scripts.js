document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const searchBtn = document.getElementById('searchBtn');
    const resultsContainer = document.getElementById('results-container');
    const originalBtnContent = searchBtn.innerHTML;

    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // --- Loading State --- 
            searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...';
            searchBtn.disabled = true;

            const formData = new FormData(searchForm);

            fetch(searchForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newResults = doc.getElementById('results-container').innerHTML;
                resultsContainer.innerHTML = newResults;
            })
            .catch(error => {
                console.error('Search error:', error);
                resultsContainer.innerHTML = '<p class="error">An unexpected error occurred. Please try again.</p>';
            })
            .finally(() => {
                // --- Reset Button State --- 
                searchBtn.innerHTML = originalBtnContent;
                searchBtn.disabled = false;
            });
        });
    }
});