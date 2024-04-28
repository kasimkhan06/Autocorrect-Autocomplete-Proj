import re
import string
from collections import Counter
import numpy as np

def read_corpus(filename):
  with open(filename, "r") as file:
    lines = file.readlines()
    words = []
    for line in lines:
      words += re.findall(r'\w+', line.lower())

  return words

words = read_corpus("./gutenberg_corpus.txt")
print(f"There are {len(words)} total words in the corpus")

vocabs = set(words)
print(f"There are {len(vocabs)} unique words in the vocabulary")

word_counts = Counter(words)
# print(word_counts["love"])

total_word_count = float(sum(word_counts.values()))
word_probas = {word: word_counts[word] / total_word_count for word in word_counts.keys()}

# print(word_probas["love"])

def split(word):
  return [(word[:i], word[i:]) for i in range(len(word) + 1)]

# print(split("trash"))

def delete(word):
  return [l + r[1:] for l,r in split(word) if r]

# print(delete("trash"))

def swap(word):
  return [l + r[1] + r[0] + r[2:] for l, r in split(word) if len(r)>1]

# print(swap("trash"))

string.ascii_lowercase

def replace(word):
  letters = string.ascii_lowercase
  return [l + c + r[1:] for l, r in split(word) if r for c in letters]

# print(replace("trash"))

def insert(word):
  letters = string.ascii_lowercase
  return [l + c + r for l, r in split(word) for c in letters]

# print(insert("trash"))

def edit1(word):
  return set(delete(word) + swap(word) + replace(word) + insert(word))

# print(edit1("trash"))

def edit2(word):
  return set(e2 for e1 in edit1(word) for e2 in edit1(e1))

# print(edit2("trash"))

def correct_spelling(word, vocabulary, word_probabilities):
  if word in vocabulary:
    print(f"{word} is already correctly spelt")
    return

  suggestions = edit1(word) or edit2(word) or [word]
  best_guesses = [w for w in suggestions if w in vocabulary]
  return [(w, word_probabilities[w]) for w in best_guesses]

# word = "mire"
# corrections = correct_spelling(word, vocabs, word_probas)

# if corrections:
#   print(corrections)
#   probs = np.array([c[1] for c in corrections])
#   best_ix = np.argmax(probs)
#   correct = corrections[best_ix][0]
#   print(f"{correct} is suggested for {word}")

class SpellChecker(object):

  def __init__(self, corpus_file_path):
    with open(corpus_file_path, "r") as file:
      lines = file.readlines()
      words = []
      for line in lines:
        words += re.findall(r'\w+', line.lower())

    self.vocabs = set(words)
    self.word_counts = Counter(words)
    total_words = float(sum(self.word_counts.values()))
    self.word_probas = {word: self.word_counts[word] / total_words for word in self.vocabs}

  def _level_one_edits(self, word):
    letters = string.ascii_lowercase
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [l + r[1:] for l,r in splits if r]
    swaps = [l + r[1] + r[0] + r[2:] for l, r in splits if len(r)>1]
    replaces = [l + c + r[1:] for l, r in splits if r for c in letters]
    inserts = [l + c + r for l, r in splits for c in letters]

    return set(deletes + swaps + replaces + inserts)

  def _level_two_edits(self, word):
    return set(e2 for e1 in self._level_one_edits(word) for e2 in self._level_one_edits(e1))

  def check(self, word):
    candidates = self._level_one_edits(word) or self._level_two_edits(word) or [word]
    valid_candidates = [w for w in candidates if w in self.vocabs]
    return sorted([(c, self.word_probas[c]) for c in valid_candidates], key=lambda tup: tup[1], reverse=True)

checker = SpellChecker("./gutenberg_corpus.txt")

# checker.check("mire")

