#!/usr/bin/python

""" Command-line password generator
    -------------------------------

    Generates secure and random passwords guaranteed to satisfy the usual
    complexity requirements as well.

    The generated passwords are of fixed length (currently 8), and guaranteed
    to consist at least one characters from each of the defined character
    categories (currently lower case, upper case and numbers).

    Homoglyphs (characters that look alike, such as "0" and "O") are not used.

    To estimate the entropy of generated passwords, run with -e argument.
"""

import random


class PasswordGenerator:
    # Character categories
    categories = [
        'abcdefghjkmnopqrstuvwxyz',
        'ABCDEFGHJKLMNPQRSTUVWXYZ',
        '23456789',
        # '_-+*!.()=&',
    ]

    # Password length
    length = 8

    def estimateCombinations(self):
        """ Estimates total number of combinations.

            This does not account for the permutations of "forced" characters, so
            the real number of combinations will be higher than this estimate.
        """

        allCharsCount = 0
        combinations = 1

        # Count combinations for the forced characters.
        for chars in self.categories:
            combinations *= len(chars)
            allCharsCount += len(chars)

        # Multiply by combinations for the unforced characters.
        combinations *= allCharsCount ** (self.length - len(self.categories))

        return combinations

    def generatePassword(self):
        allCharacters = ''.join(self.categories)

        # Start with a password makeup where each character is picked freely among allCharacters.
        passwordMakeup = [ allCharacters ] * self.length

        # For each category, we now force one random character to be from that specific category.
        forcedIndexes = random.sample(xrange(self.length), len(self.categories))

        for i, chars in zip(forcedIndexes, self.categories):
            passwordMakeup[i] = chars

        return ''.join(map(random.choice, passwordMakeup))

# Command-line interface

if __name__ == '__main__':
    import math
    import sys

    g = PasswordGenerator()

    if len(sys.argv) == 2 and sys.argv[1] == '-e':
        combinations = g.estimateCombinations()
        print 'More than %s combinations ~ %.1f bits of entropy.' % (combinations, math.log(combinations, 2))
        sys.exit(0)

    print g.generatePassword()
