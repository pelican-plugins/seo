""" Analyze the internal link of an article. """

from bs4 import BeautifulSoup


class InternalLinkAnalyzer():
    """ Analyze internal link of an article. """

    def __init__(self, content, siteurl):
        self._soup = BeautifulSoup(content, features="html.parser")
        self._links = self._soup.find_all('a')
        self._siteurl = siteurl

    def has_internal_link(self):
        """
        Return True is there is a internal link.
        Need to have SITEURL parameter declared.
        """

        if not self._links:
            return False

        for link in self._links:
            if self._siteurl in link['href']:
                return True

        return False

    @property
    def internal_link_occurrence(self):
        """ Return the internal link occurrence. """

        return len([link for link in self._links if self._siteurl in link['href']])
