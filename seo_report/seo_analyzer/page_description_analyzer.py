""" Analyze the page description. """

class PageDescriptionAnalyzer():
    """ Analyze the page description. """

    def __init__(self, metadata):
        self.page_description = metadata.get('description', None)

    def has_page_description(self):
        """ Return True if there is a page description. """

        if not self.page_description:
            return False

        return True

    @property
    def page_description_length(self):
        """ Return page description length. """

        return len(self.page_description)
