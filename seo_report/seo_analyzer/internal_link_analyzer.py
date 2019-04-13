""" Analyze the internal link of an article. """

from bs4 import BeautifulSoup

class InternalLinkAnalyzer():
    """ Analyze internal link of an article. """

    def __init__(self, article):
        _content = getattr(article, 'content', None)
        self._settings = getattr(article, 'settings', None)
        self._content_soup = BeautifulSoup(_content, features="html.parser")
        self._links = self._content_soup.find_all('a')

    def has_internal_link(self):
        """ Return True is there is a internal link. Need to have SITEURL parameter declared. """

        if not self._links:
            return False

        for link in self._links:
            if self._settings['SITEURL'] in link['href']:
                return True

        return False

    @property
    def internal_link_occurrence(self):
        """ Return the internal link occurrence. """

        return len([link for link in self._links if self._settings['SITEURL'] in link['href']])
