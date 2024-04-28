document.addEventListener('DOMContentLoaded', function () {
    const wordInput = document.getElementById('word');
    const autocompletePrefixInput = document.getElementById('autocomplete-prefix'); // New line
    const autocompleteSuggestionsDiv = document.getElementById('autocomplete-suggestions'); // New line

    autocompletePrefixInput.addEventListener('input', function () { // New event listener for input change
        const prefix = autocompletePrefixInput.value.trim();
        if (prefix === '') {
            autocompleteSuggestionsDiv.innerHTML = '';
            return;
        }

        fetch('/autocomplete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prefix: prefix })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            displayAutocompleteSuggestions(data.suggestions);
        })
        .catch(error => {
            console.error('Error fetching autocomplete data:', error);
            autocompleteSuggestionsDiv.innerHTML = '<p>An error occurred while fetching autocomplete suggestions.</p>';
        });
    });


    function displayAutocompleteSuggestions(suggestions) {
        autocompleteSuggestionsDiv.innerHTML = '';
        if (suggestions.length === 0) {
            autocompleteSuggestionsDiv.innerHTML = '<p>No autocomplete suggestions found.</p>';
            return;
        }
        const ul = document.createElement('ul');
        suggestions.forEach(suggestion => {
            const li = document.createElement('li');
            li.textContent = suggestion;
            ul.appendChild(li);
        });
        autocompleteSuggestionsDiv.appendChild(ul);
    }
});
