# Instructions

- create book given wuxiaworld tabel of contents link
  
  `book = WuxiaWorld("https://www.wuxiaworld.com/novel/the-charm-of-soul-pets")`
    
- save to epub format
  
    `create_epub(book)`

# Returns

We will get 2 files, `book.epub` and `navMap.txt`

- use a epub editor file and replace the `<navmap>` tag inside `book.epub/EPUB/toc.ncx` with the contents of navMap.txt