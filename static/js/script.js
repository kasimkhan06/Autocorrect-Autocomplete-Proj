document.addEventListener('DOMContentLoaded', function () {
    const wordInput = document.getElementById('word');
    const checkBtn = document.getElementById('check-btn');
    const correctionsDiv = document.getElementById('corrections');

    checkBtn.addEventListener('click', function () {
        const word = wordInput.value.trim();
        if (word === '') {
            alert('Please enter a word to spell-check.');
            return;
        }

        fetch('/spellcheck', {
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

    // function displayCorrections(corrections) {
    //     correctionsDiv.innerHTML = '';
    //     if (corrections.length === 0) {
    //         correctionsDiv.innerHTML = '<p>No corrections found.</p>';
    //         return;
    //     }
    //     const ul = document.createElement('ul');
    //     corrections.forEach(correction => {
    //         const li = document.createElement('li');
    //         li.textContent = `${correction[0]} (Probability: ${correction[1].toFixed(4)})`;
    //         ul.appendChild(li);
    //     });
    //     correctionsDiv.appendChild(ul);
    // }

    function displayCorrections(corrections) {
        correctionsDiv.innerHTML = '';
        if (corrections.length === 0) {
            correctionsDiv.innerHTML = '<p>No corrections found.</p>';
            return;
        }
        const ul = document.createElement('ul');
        corrections.forEach(correction => {
            const li = document.createElement('li');
            const probability = Number(correction[1]).toFixed(10); // Format probability to 10 decimal places
            li.textContent = `${correction[0]} (Probability: ${probability})`;
            ul.appendChild(li);
        });
        correctionsDiv.appendChild(ul);
    }
    
});
