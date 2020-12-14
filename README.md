# Instructions

Call main function given the associated Wuxiaworld table of contents link 

- `python3 main.py "https://www.wuxiaworld.com/novel/above-your-head"`

# Post Processing

We will get 2 files, `book.epub` and `navMap.txt`

- use an epub editor and replace the `<navmap>` tag inside `book.epub/EPUB/toc.ncx` with the contents of `navMap.txt`