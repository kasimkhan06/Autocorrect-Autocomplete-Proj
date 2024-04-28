document.addEventListener('DOMContentLoaded', function () {

    const autocompletePrefixInput = document.getElementById('autocomplete-prefix'); // New line
    const autocompleteSuggestionsDiv = document.getElementById('autocomplete-suggestions'); // New line


    autocompletePrefixInput.addEventListener('input', function () {
        const prefix = autocompletePrefixInput.value.trim();
        if (prefix === '') {
            autocompleteSuggestionsDiv.innerHTML = '';
            return;
        }
        console.log(prefix);
        fetch('/autocomplete/suggest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify({ prefix: prefix })
        })
            .then(response => {
                //console log 
                console.log(response);
                return response.json();
            })
            .then(data => {
                console.log(data);
                displayAutocompleteSuggestion(data.suggestions);
            })
            .catch(error => {
                console.error('Error fetching autocomplete data:', error);
                autocompleteSuggestionsDiv.innerHTML = '<p>An error occurred while fetching autocomplete suggestions.</p>';
            });
    });

    function displayAutocompleteSuggestion(suggestion) {
        autocompleteSuggestionsDiv.innerHTML = '';
        if (!suggestion) {
            autocompleteSuggestionsDiv.innerHTML = '<p class="text-muted">No autocomplete suggestion found.</p>';
            return;
        }
        const p = document.createElement('p');
        p.classList.add('mb-0'); // Add Bootstrap margin class to remove bottom margin
        p.textContent = suggestion;
        autocompleteSuggestionsDiv.appendChild(p);
    }


});
