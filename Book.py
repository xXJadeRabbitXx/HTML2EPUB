from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

"""
    The purpose of this class is so I can abstract away the html layers
    It provide an interface so I can get 
        title, 
        chapter contents 
    without worrying about website format
"""


class Book(ABC):

    @abstractmethod
    def get_title(self):
        pass

    @abstractmethod
    def get_current_chapter_and_increment(self):
        pass


class WuxiaWorld(Book):
    def __init__(self, table_of_contents_url):
        self.base_url = "https://www.wuxiaworld.com"

        # fake header to include with HTML request
        # WuxiaWorld blocks requests with no headers
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"

        table_of_contents_request = requests.get(table_of_contents_url, headers={'User-Agent': self.user_agent})

        if table_of_contents_request.status_code == 200:
            table_of_contents_html = BeautifulSoup(table_of_contents_request.text, 'html.parser')
        else:
            print(table_of_contents_request.status_code)
            raise RuntimeError("problem fetching table of contents: " + table_of_contents_url)

        self.title = table_of_contents_html.title.text
        self.toc_chapter_list = self.__find_all_chapter_url_from_toc(table_of_contents_html)
        self.next_chapter = self.toc_chapter_list.pop(0)
        self.chapter_index = 1

    def __find_all_chapter_url_from_toc(self, table_of_contents_html):
        chapter_list = table_of_contents_html.body.find_all(class_="chapter-item")

        result = []

        for chapter in chapter_list:
            chapter_title = chapter.find("a").text.strip()
            chapter_url = chapter.find("a")["href"]

            result.append({"title": chapter_title, "url": self.base_url + chapter_url})

        return result

    def get_title(self):
        return self.title

    def get_current_chapter_and_increment(self):
        current_chapter_url = self.next_chapter["url"]
        current_chapter_name = self.next_chapter["title"]

        chapter_data_request = requests.get(current_chapter_url, headers={'User-Agent': self.user_agent})

        if chapter_data_request.status_code == 200:
            # getting current chapter data
            chapter_data_html = BeautifulSoup(chapter_data_request.text, 'html.parser')
            chapter_data = self.__get_chapter_data(chapter_data_html)
        else:
            # skipping chapter
            print(str(chapter_data_request.status_code) + " Failed to retrieve chapter " + current_chapter_name)
            return {"name": current_chapter_name, "content": ""}

        # Updating next chapter
        self.next_chapter = self.toc_chapter_list.pop(0)
        self.chapter_index = self.chapter_index+1

        return {"title": current_chapter_name, "content": chapter_data}

    @staticmethod
    def __get_chapter_data(chapter_html_data):
        chapter_content = chapter_html_data.body.find("div", {"id": "chapter-content"}).find_all("p")

        clean_content = [line.text.strip() for line in chapter_content]

        return clean_content
