#!/usr/bin/env python3

import random
import string
from collections import defaultdict


def remove_punctuation(text):
    table = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    return text.translate(table)


def is_preposition(token):
    with open('prepositions.txt') as prepositions:
        return token.lower() in prepositions.read().split()


# Should handle conjunctions that are more than a word long!
def is_conjunction(token):
    with open('conjunctions.txt') as conjunctions:
        return token.lower() in conjunctions.read().split('\n')  # Needed


def is_article(token):
    return token.lower() in ('a', 'an', 'the')


def is_good_ending(token):
    return not is_article(token) and not is_preposition(token) and not is_conjunction(token)


def is_number(token):
    for character in token:
        if not character.isdigit():
            return False
    return True


def remove_numbers(words):
    # Currently just removes integers
    result = []
    for word in words:
        if not is_number(word):
            result.append(word)
    return result


def make_sentence(table):
    # Get a random word from the body
    sentence = [random.choice(list(table.keys()))[0]]
    while len(sentence) < 8 or not is_good_ending(sentence[-1]):
        best_so_far = None
        for key in table.keys():
            if key[0] == sentence[-1]:
                if (best_so_far is None) or (table[key] > best_so_far[1]):
                    if random.random() > random.random():
                        best_so_far = (key[1], table[key])
        if best_so_far is not None:
            sentence.append(best_so_far[0])
    return ' '.join(sentence)


def main():
    with open('corpus.txt') as corpus:
        text = corpus.read()
        text = text.lower()
        text = remove_punctuation(text)
        words = text.split()
        words = remove_numbers(words)
        table = defaultdict(lambda: 0)
        for i in range(len(words) - 1):
            table[tuple(words[i:i + 2])] += 1
        for i in range(10):
            print(make_sentence(table))


if __name__ == '__main__':
    main()
