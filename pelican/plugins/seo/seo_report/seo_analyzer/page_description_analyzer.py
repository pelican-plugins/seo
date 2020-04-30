""" Analyze the page description. """


class PageDescriptionAnalyzer():
    """ Analyze the page description. """

    def __init__(self, description):
        self._description = description

    def has_page_description(self):
        """ Return True if there is a page description. """

        if not self._description:
            return False

        return True

    @property
    def page_description_length(self):
        """ Return page description length. """

        return len(self._description)
