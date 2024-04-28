document.addEventListener('DOMContentLoaded', function () {

    const wordInput = document.getElementById('word');
    const checkBtn = document.getElementById('check-btn');
    const correctionsDiv = document.getElementById('corrections');


    // if enter key is pressed, trigger the click event of the check button
    wordInput.addEventListener('keyup', function (event) {
        if (event.key === 'Enter') {
            checkBtn.click();
        }
    }
    );

    checkBtn.addEventListener('click', function () {
        const word = wordInput.value.trim();
        if (word === '') {
            alert('Please enter a word to spell-check.');
            return;
        }

        fetch('/spellchecker/check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ word: word })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                displayCorrections(data.corrections);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                alert('An error occurred while spell-checking the word.');
            });
    });

    function displayCorrections(corrections) {
        correctionsDiv.innerHTML = '';
        if (corrections.length === 0) {
            correctionsDiv.innerHTML = '<p class="text-muted">No corrections found.</p>';
            return;
        }

        //limit the number of corrections to 10 
        corrections = corrections.slice(0, 10);
        
        const ul = document.createElement('ul');
        ul.classList.add('list-group'); // Add Bootstrap list-group class
        //add bottom margin to the list
        ul.classList.add('mb-3');
        corrections.forEach(correction => {
            const li = document.createElement('li');
            li.classList.add('list-group-item'); // Add Bootstrap list-group-item class
            const probability = Number(correction[1]).toFixed(10); // Format probability to 10 decimal places
            li.textContent = `${correction[0]} (Probability: ${probability})`;
            ul.appendChild(li);
        });
        correctionsDiv.appendChild(ul);
    }


});
