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

    """
        I'm not sure how to use the Table of Contents in the EPUB library, so I'm manually generating the navMap
        This result needs to be merged into the epub ncx later
    """
    nav_map = ElementTree.Element("navMap")

    total_chapters = len(source.toc_chapter_list) + 1
    print("Total chapters: " + str(total_chapters))
    print("Processing chapters ...")

    # creating chapters
    for i in range(total_chapters):
        current_chapter = source.chapter_index
        data = source.get_current_chapter_and_increment()

        print(data["title"])

        # formatting chapter content into appropriate HTML for epub library
        processed_content = ["<p>" + line + "</p>" for line in data["content"]]
        content = "".join(processed_content)
        title = "<h1>" + data["title"] + "</h1>"

        final_content = "<html><body>" + title + content + "</body></html>"
        chapter_name = "chapter_" + str(current_chapter-1)

        # creating the actual epub chapter based on HTML content
        chapter = epub.EpubHtml(title=data["title"], file_name=chapter_name+".xhtml", lang='en')
        chapter.set_content(final_content)

        book.add_item(chapter)
        chapters.append(chapter)

        # generating associated navmap
        nav_point = ElementTree.SubElement(nav_map, "navPoint")
        nav_point.attrib["id"] = chapter_name
        nav_point.attrib["playOrder"] = str(current_chapter)

        nav_label = ElementTree.SubElement(nav_point, "navLabel")
        nav_label_text = ElementTree.SubElement(nav_label, "text")
        nav_label_text.text = data["title"]
        content = ElementTree.SubElement(nav_point, "Content")
        content.attrib["src"] = chapter_name + ".xhtml"

        # waits 1 second before processing next chapter
        # just in case there's some traffic volume throttle
        time.sleep(1)

    # define CSS style
    style = 'BODY {color: white;}'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

    # add CSS file
    book.add_item(nav_css)

    # supposed to define Table Of Contents here, but can't get it to work -- see above comment

    # basic spine
    chapters.insert(0, "nav")
    book.spine = chapters

    # add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # write to the file
    epub.write_epub('book.epub', book, {})

    root = ElementTree.ElementTree(nav_map)
    root.write("navMap.txt")
