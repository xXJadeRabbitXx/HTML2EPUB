from Book import *
from create_epub import create_epub


def main():
    book = WuxiaWorld("https://www.wuxiaworld.com/novel/the-charm-of-soul-pets")
    create_epub(book)
    print("done")


if __name__ == '__main__':
    main()
