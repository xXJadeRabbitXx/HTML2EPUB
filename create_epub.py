"""
    This module is in charge of taking in a abstract "website" and turning it into an epub
"""

from ebooklib import epub
import time
import xml.etree.ElementTree as ElementTree

def create_epub(source):
    book = epub.EpubBook()

    book.set_language("en")
    book.set_title(source.get_title())

    chapters = []
    navMap = ElementTree.Element("navMap")

    # creating chapters
    while len(source.toc_chapter_list) > 0:
        current_chapter = source.chapter_index
        data = source.get_current_chapter_and_increment()

        content = "".join(data["content"])
        title = "<h1>" + data["title"] + "</h1>"

        final_content = "<html><body>" + title + content + "</body></html>"
        chapter_name = "chapter_" + str(current_chapter-1)

        chapter = epub.EpubHtml(title=data["title"], file_name= chapter_name+".xhtml", lang='en')
        chapter.set_content(final_content)

        book.add_item(chapter)
        chapters.append(chapter)

        navPoint = ElementTree.SubElement(navMap, "navPoint")
        navPoint.attrib["id"] = chapter_name
        navPoint.attrib["playOrder"] = str(current_chapter)

        navLabel = ElementTree.SubElement(navPoint, "navLabel")
        navLabel_text = ElementTree.SubElement(navLabel, "text")
        navLabel_text.text = data["title"]
        content = ElementTree.SubElement(navPoint, "Content")
        content.attrib["src"] = chapter_name + ".xhtml"

        if current_chapter % 10 == 0:
            print(current_chapter)

        time.sleep(1)

    # define CSS style
    style = 'BODY {color: white;}'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

    # add CSS file
    book.add_item(nav_css)

    # define Table Of Contents can't get it to work
    #chapters.insert(0, toc)
    #book.toc = (epub.Link('toc.xhtml', 'Introduction', 'intro'),
    #            epub.Section('Table of Contents'), tuple(chapters))

    # basic spine
    chapters.insert(0, "nav")
    book.spine = chapters

    # add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # write to the file
    epub.write_epub('book.epub', book, {})

    root = ElementTree.ElementTree(navMap)
    root.write("navMap.txt")