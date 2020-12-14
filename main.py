from Book import *
from create_epub import create_epub
import sys


def main(url):
    book = WuxiaWorld(url)
    create_epub(book)
    print("done")


if __name__ == '__main__':
    main(sys.argv[1])
