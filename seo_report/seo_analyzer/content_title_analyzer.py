""" Analyze the content title. """

from bs4 import BeautifulSoup

class ContentTitleAnalyzer():
    """ Analyze the content title. """

    def __init__(self, article):
        _content = getattr(article, 'content', None)
        self.content_soup = BeautifulSoup(_content, features="html.parser")

    def has_content_title(self):
        """ Return True is there is a content title. """

        if not self.content_soup.h1:
            return False

        return True

    def is_content_title_unique(self):
        """ Return True if content title is unique. """

        content_titles = self.content_soup.find_all('h1')

        if len(content_titles) > 1:
            return False

        return True
