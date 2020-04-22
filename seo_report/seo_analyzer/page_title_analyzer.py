""" Analyze the page title. """


class PageTitleAnalyzer():
    """ Analyze the page title. """

    def __init__(self, title):
        self._title = title

    def has_page_title(self):
        """ Return True is there is a page title. """

        if not self._title:
            return False

        return True

    @property
    def page_title_length(self):
        """ Return page title length. """

        return len(self._title)
