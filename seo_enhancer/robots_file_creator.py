""" Return elements to build the robots.txt file. """


class RobotsFileCreator():
    """ Get robots rules from article metadata. Return them. """

    def __init__(self, metadata):
        self.metadata_noindex = metadata.get('noindex')
        self.metadata_disallow = metadata.get('disallow')

    @property
    def get_noindex(self):
        """ Return noindex rules. """

        return self.metadata_noindex

    @property
    def get_disallow(self):
        """ Return disallow rules. """

        return self.metadata_disallow
