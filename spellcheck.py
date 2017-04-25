#!/usr/bin/env python3
"""
.. module:: spellcheck
    :synopsis: A simple spell checking module

.. moduleauthor:: Matthew Emerson <emersonmde@gmail.com>

"""

from collections import OrderedDict
import string
import timeit

class Node:
    """This class builds up a trie of nodes to store unique words.

    Each node, except for the root node, contains a letter, list of
    children and an end marker. There will be a child node for each consecutive
    letter in a word. When looking up a word we just walk the list one letter
    at a time.

        :param letter: The letter for this node.
        :type letter: string.
        :param end: Designates the end of a word.
        :type end: bool.
        :param sortdict: Designates whether or not to sort the children dict.
        :type sortdict: bool.


    """

    sortdict = True

    def __init__(self, letter='', end=False, sortdict=True):
        if sortdict:
            self.children = OrderedDict()
        else:
            Node.sortdict = False
            self.children = {}
        self.letter = letter
        self.end = end
        self.sortdict = sortdict

    def add_word(self, word):
        """Add a string or word to the trie.

        This is a recursive method that uses the first letter for a child node
        then passes the remaining string down the trie.

            :param word: The word or remaining string to be added.
            :type word: string.
            :returns: False if the word or string is omitted.

        """

        if not word:
            return False
        key = word[:1]
        if key not in self.children:
            self.children[key] = Node(key)
        if len(word) >= 2: # 2 or more chars
            self.children[key].add_word(word[1:])
        else: # 1 char
            self.children[key].end = True

    def lookup(self, word):
        if not word:
            return False
        if not self.letter:
            if word[:1] in self.children:
                return self.children[word[:1]].lookup(word)
        elif len(word) == 1:
            if self.letter == word and self.end:
                return True
            else:
                return False
        elif len(word) >= 2:
            if (self.letter == word[:1]) and (word[1:2] in self.children):
                return self.children[word[1:2]].lookup(word[1:])
            else:
                return False
                
    def walk(self, prefix=''):
        if self.sortdict:
            self.children = OrderedDict(sorted(self.children.items(), key=lambda d: d[0]))
        if self.letter:
            prefix += str(self.letter)
            if self.end:
                yield prefix
        for key, node in self.children.items():
            yield from node.walk(prefix)


class Dictionary:
    def __init__(self, filename=None, encoding='iso-8859-1'):
        self.root = Node(sortdict=True)
        self.encoding = encoding
        with open(filename, 'r', encoding=self.encoding) as infile:
            for line in infile:
                self.root.add_word(line.encode(self.encoding).strip().lower())

    def __str__(self):
        return str(', '.join(self.root.walk()))

    def add_word(self, word):
        self.root.add_word(word.encode(self.encoding))

    def lookup(self, word):
        return self.root.lookup(word.encode(self.encoding))

def check_input(dictionary):

    intext = input("Input text to be spell checked: ")

    translator = str.maketrans('', '', string.punctuation.replace("'", ""))
    words = intext.translate(translator).split(' ')

    for word in words:
        if not dictionary.lookup(word.lower()):
            print("'{}' not found".format(word))
        else:
            #print("{} found".format(word))
            pass


if __name__ == '__main__':

    d1 = Dictionary("10000.txt")

    check_input(d1)
