import os
import sys


if __name__ == '__main__':
    text = []
    books_dir = os.path.join(os.path.dirname(__file__), 'books')
    for book in os.listdir(books_dir):
        with open(os.path.join(books_dir, book)) as book_file:
            text.append(book_file.read())
    with open('corpus.txt', 'w') as corpus:
        corpus.write('\n'.join(text))
