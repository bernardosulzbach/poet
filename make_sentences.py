#!/usr/bin/env python3

import random
import string
from collections import defaultdict


def remove_punctuation(text):
    table = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    return text.translate(table)


def is_preposition(token):
    """
    Returns whether or not the provided token is a preposition.
    :param token: a single word
    """
    with open('prepositions.txt') as prepositions:
        return token.lower() in prepositions.read().split('\n')


def is_conjunction(sentence):
    """
    Returns whether or not the provided sequence of words is a conjunction.
    :param sentence: a list of words
    """
    with open('conjunctions.txt') as conjunctions:
        words = ' '.join(sentence).lower()
        return words in conjunctions.read().split('\n')


def ends_in_conjunction(sentence):
    """
    Evaluates if the specified sentence ends with a conjunction.
    :param sentence: a list of words
    """
    # Relies on the fact that the biggest conjunction has three words.
    biggest_number_of_words_in_a_conjunction = 3
    for i in range(min(len(sentence), biggest_number_of_words_in_a_conjunction)):
        if is_conjunction(sentence[-(i + 1):]):
            return True
    return False


def is_article(token):
    return token.lower() in ('a', 'an', 'the')


def has_good_ending(sentence):
    """
    Evaluates whether or not the sentence has a good ending.
    :param sentence: an iterable of words
    """
    last_token = sentence[-1]
    if not is_article(last_token):
        if not is_preposition(last_token):
            if not ends_in_conjunction(sentence):
                return True
    return False


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


def make_sentence(table, minimum_sentence_length=6):
    # Get a random word from the body
    sentence = [random.choice(list(table.keys()))[0]]
    while len(sentence) < minimum_sentence_length or not has_good_ending(sentence):
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
