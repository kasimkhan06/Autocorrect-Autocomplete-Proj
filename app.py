from flask import Flask, render_template, request, jsonify
from spell_checker import SpellChecker

app = Flask(__name__)
checker = SpellChecker("./big.txt")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spellcheck', methods=['POST'])
def spellcheck():
    data = request.get_json()
    word = data.get('word')
    if not word:
        return jsonify({'error': 'Word not provided'}), 400
    
    corrections = checker.check(word)
    return jsonify({'corrections': corrections})

if __name__ == '__main__':
    app.run(debug=True)
