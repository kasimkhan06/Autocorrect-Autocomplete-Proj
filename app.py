import os
from spell_checker import SpellChecker
from flask import Flask, render_template, request, jsonify
from autocomplete import Autocomplete,Trie, TrieNode  # Import Autocomplete class

app = Flask(__name__)

autocomplete = Autocomplete()  # Initialize Autocomplete
checker = SpellChecker("./gutenberg_corpus.txt") # Initialize SpellChecker

@app.route('/')  
def index():
    return render_template('index.html')

@app.route('/autocomplete')
def autocomplete_page():
    return render_template('autocomplete.html')

@app.route('/spellchecker')
def spellchecker_page():
    return render_template('spellchecker.html')


@app.route('/autocomplete/suggest', methods=['POST'])
def suggest_autocomplete():
    data = request.get_json()
    prefix = data.get('prefix')
    if not prefix:
        return jsonify({'ERROR': 'No prefix provided'}), 400
    
    suggestions = autocomplete.suggestWord(prefix)
    return jsonify({'suggestions': suggestions})

@app.route('/spellchecker/check', methods=['POST'])
def check_spellchecker():
    data = request.get_json()
    word = data.get('word')
    if not word:
        return jsonify({'corrections': []})
    
    corrections = checker.check(word)
    return jsonify({'corrections': corrections})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
