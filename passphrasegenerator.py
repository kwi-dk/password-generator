#!/usr/bin/python

""" Command-line passphrase generator
    =================================

    Generates secure and random passphrases consisting simply of four random
    dictionary words, loosely based on [Munroe11].

    To estimate the entropy of generated passwords, run with -e argument.

    Recipe for producing word list
    ------------------------------

    Prepare a list of nouns using the WordNet database of English [WordNet06]:
    grep -v '^ ' dict/data.noun|cut -d ' ' -f 5|grep -v '_'|sort|uniq > nouns.txt

    For a list of common words in modern language, a frequency list based on TV
    and movie scripts was consulted [Wiktionary], and the top 6000 words
    extracted to the file top6000.txt.

    Of the top 6000 word list, only nouns were kept by matching against the
    WordNet list of nouns, yielding 2646 words:

    grep -x -F -f top6000.txt nouns.txt > words.txt

    Finally, various odd words, numbers and bad words were removed. These are
    specified in badwords.txt. This leaves 2027 good words.

    grep -x -v -F -f badwords.txt words.txt > goodwords.txt

    (Bad words are words that might yield inappropriate or offensive sentences,
    such as proper names and references to crime, violence, anatomy, sexuality,
    religion, drugs, family relations, illness and death.)


    References
    ----------

    [Munroe11]   Password Strength. Randall Munroe, XKCD #936.
                 http://www.xkcd.com/936/

    [WordNet06]  WordNet 3.0 for UNIX-like systems, just database files
                 http://wordnetcode.princeton.edu/3.0/WNdb-3.0.tar.gz

    [Wiktionary] Frequency lists: TV and movie scripts. Wiktionary.
                 http://en.wiktionary.org/w/index.php?title=Wiktionary:Frequency_lists&oldid=15589879#TV_and_movie_scripts
"""

import random

# Use the OS secure random generator (/dev/urandom or CryptGenRandom).
random = random.SystemRandom()


class PassphraseGenerator:
    words = None
    length = 4 # passphrase length, in words

    def __init__(self, words):
        self.words = words

    def calculateCombinations(self):
        """ Calculates total number of combinations. """

        return len(self.words) ** self.length

    def generatePassword(self):
        return ' '.join(random.choice(self.words) for i in range(self.length))

# Command-line interface

if __name__ == '__main__':
    import argparse
    import math
    import sys

    # Parse arguments
    parser = argparse.ArgumentParser(description='Generates a random passphrase.')
    parser.add_argument('dictionary', nargs='?', default='goodwords.txt',
        help='word list to use (default: goodwords.txt)')
    parser.add_argument('-e', '--entropy', action='store_true',
        help='estimate the entropy of the generated passphrase')
    args = parser.parse_args()

    with open(args.dictionary, 'r') as f:
        g = PassphraseGenerator(f.read().split('\n'))

    if args.entropy:
        combinations = g.calculateCombinations()
        print('%s combinations ~ %.1f bits of entropy.' % (combinations, math.log(combinations, 2)))
    else:
        print(g.generatePassword())
