from unittest import TestCase

import sentence_generator


class TestMakeSentences(TestCase):
    def test_remove_punctuation(self):
        sentence = "Alice said: \"Give me 'the' rabbit's head!\"."
        expected = "Alice said Give me the rabbit's head"
        self.assertEqual(expected, sentence_generator.remove_punctuation(sentence).strip())
