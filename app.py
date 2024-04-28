# import os
# from flask import Flask, render_template, request, jsonify
# from spell_checker import SpellChecker

# app = Flask(__name__)
# checker = SpellChecker("./gutenberg_corpus.txt")

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/spellcheck', methods=['POST'])
# def spellcheck():
#     data = request.get_json()
#     word = data.get('word')
#     if not word:
#         return jsonify({'error': 'Word not provided'}), 400
    
#     corrections = checker.check(word)
#     return jsonify({'corrections': corrections})

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)


import os
from flask import Flask, render_template, request, jsonify
from autocomplete import Autocomplete,Trie, TrieNode  # Import Autocomplete class

app = Flask(__name__)

autocomplete_instance = Autocomplete()  # Initialize Autocomplete

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/autocomplete', methods=['POST'])  # Change route to /autocomplete
def autocomplete_handler():  # Renamed the function
    data = request.get_json()
    prefix = data.get('prefix')
    if not prefix:
        return jsonify({'error': 'Prefix not provided'}), 400
    
    suggestions = autocomplete_instance.suggestWord(prefix)  # Use the instance method
    return jsonify({'suggestions': suggestions})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
