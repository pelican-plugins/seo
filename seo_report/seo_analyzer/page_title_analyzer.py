""" Analyze the page title. """

class PageTitleAnalyzer():
    """ Analyze the page title. """

    def __init__(self, metadata):
        self.page_title = metadata.get('title', None)

    def has_page_title(self):
        """ Return True is there is a page title. """

        if not self.page_title:
            return False

        return True

    @property
    def page_title_length(self):
        """ Return page title length. """

        return len(self.page_title)
