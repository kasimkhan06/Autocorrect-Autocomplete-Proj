import pickle
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def search(self, prefix):
        if not self.root.children:
            return []
        
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._get_words_with_prefix(node, prefix)
    
    def _get_words_with_prefix(self, node, prefix):
        words = []
        if node.is_end_of_word:
            words.append(prefix)
        for char, child_node in node.children.items():
            words.extend(self._get_words_with_prefix(child_node, prefix + char))
        return words

class Autocomplete:

    def __init__(self):
        # Initialize trie, word_occ, and word_prob
        self.trie = Trie() 
        self.word_occurrences = None
        self.word_probabilities = None

        # Load data from pickle file
        with open('data.pkl', 'rb') as f:
            self.word_probabilities = pickle.load(f)
            self.word_occurrences = pickle.load(f)
            self.trie = pickle.load(f)

    def suggestWord(self ,prefix):
        suggestions = self.trie.search(prefix)
        #build the suggestions probability map
        suggestions_probability = {}
        for sugg in suggestions:
            suggestions_probability[sugg] = self.word_probabilities[sugg]

        sorted_suggested_words = sorted(suggestions_probability.items(), key=lambda x: x[1], reverse=True)
        if sorted_suggested_words:
            suggested_words = sorted_suggested_words
        else :
            suggested_words = []
        
        return suggested_words
