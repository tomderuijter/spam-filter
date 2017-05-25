from .base import BaseTextTokenizer
import re


class SimpleTextTokenizer(BaseTextTokenizer):

    def tokenize(self, text):
        assert isinstance(text, str)

        text = text.lower()
        tokens = split_words(text)
        tokens = filter_word_length(tokens, minimum_length=4)
        return tokens


def split_words(message):
    """
    Splits a string into words on non-alphanumerical characters.
    Benchmark taken from
    https://stackoverflow.com/questions/1276764/stripping-everything-but-alphanumeric-chars-from-a-string-in-python.
    """
    pattern = re.compile('[\W_]+')
    return pattern.split(message)


def filter_word_length(words, minimum_length=4):
    """
    Remove words shorter than a specified length.

    Language indifferent substitute for stop word filter.
    """
    return list(
        filter(
            lambda w: len(w) >= minimum_length,
            words
        )
    )
