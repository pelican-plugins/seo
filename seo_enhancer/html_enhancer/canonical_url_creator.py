""" Canonical URL creator. """

import os


class CanonicalURLCreator():
    """ Canonical URL creator. """

    def __init__(self, fileurl, siteurl):
        self._fileurl = fileurl
        self._siteurl = siteurl

    def create_url(self):
        """ Join site URL and file URL to create canonical link. """

        canonical_url = os.path.join(self._siteurl, self._fileurl)
        return canonical_url
