#!/usr/bin/env python3

import random
import re
from collections import defaultdict

preposition_list = open('prepositions.txt').read().split('\n')
conjunction_list = open('conjunctions.txt').read().split('\n')


# Improvement: do not keep a bi-gram if the words are separated by a period.
def remove_punctuation(text):
    return re.sub("[^\w]+'|'[^\w]+|[^\w']+", " ", text)


def is_preposition(token):
    """
    Returns whether or not the provided token is a preposition.
    :param token: a single word
    """
    return token.lower() in preposition_list


def is_conjunction(sentence):
    """
    Returns whether or not the provided sequence of words is a conjunction.
    :param sentence: a list of words
    """
    words = ' '.join(sentence).lower()
    return words in conjunction_list


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


def make_probability_table(unigram_count, bigram_count):
    probability_table = dict(bigram_count)
    for key in probability_table:
        probability_table[key] /= unigram_count[key[0]]
    return probability_table


def get_next_token(word, table):
    """
    Based on a probability table and a word, randomly picks a word that could follow the provided word.

    :param table: a probability table of bigrams
    :param word: a unigram
    """
    choices = {}
    for bigram, probability in table.items():
        if word == bigram[0]:
            choices[bigram[1]] = probability
    if len(choices) == 0:
        return "<IMPOSSIBLE>"
    else:
        words = list(choices.keys())
        values = list(choices.values())
        value_sum = sum(values)
        magic_number = random.random() * value_sum
        chosen_word_index = -1
        while magic_number > 0:
            chosen_word_index += 1
            magic_number -= values[chosen_word_index]
        return words[chosen_word_index]


def make_sentence(table, minimum_sentence_length=6):
    # Get a random word from the body
    sentence = [random.choice(list(table.keys()))[0]]
    while len(sentence) < minimum_sentence_length or not has_good_ending(sentence):
        sentence.append(get_next_token(sentence[-1], table))
    return ' '.join(sentence)


def main():
    with open('corpus.txt') as corpus:
        text = corpus.read()
        text = text.lower()
        text = remove_punctuation(text)
        words = text.split()
        words = remove_numbers(words)
        unigram_table = defaultdict(lambda: 0)
        bigram_table = defaultdict(lambda: 0)
        for i in range(len(words) - 1):
            unigram_table[words[i]] += 1
            bigram_table[tuple(words[i:i + 2])] += 1
        probability_table = make_probability_table(unigram_table, bigram_table)
        for i in range(10):
            print(make_sentence(probability_table))


if __name__ == '__main__':
    main()
