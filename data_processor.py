import os
import re


def remove_project_gutenberg_text(book_text):
    """
    Removes metadata from a Project Gutenberg file.
    """
    start_tag = ".*?\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .*?\*\*\*"
    end_tag = "\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .*?\*\*\*.*"
    book_text = re.sub(start_tag, "", book_text, flags=re.DOTALL)
    book_text = re.sub(end_tag, "", book_text, flags=re.DOTALL)
    return book_text


if __name__ == '__main__':
    text = []
    books_dir = os.path.join(os.path.dirname(__file__), 'books')
    for book in os.listdir(books_dir):
        with open(os.path.join(books_dir, book)) as book_file:
            text.append(remove_project_gutenberg_text(book_file.read()))
    with open('corpus.txt', 'w') as corpus:
        corpus.write('\n'.join(text))
