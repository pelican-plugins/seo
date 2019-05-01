""" Canonical URL creator. """

import os

class CanonicalURLCreator():
    """ Canonical URL creator. """

    def __init__(self, file_url, site_url):
        self._file_url = file_url
        self._site_url = site_url

    def create_url(self):
        """ Join site URL and file URL to create canonical link. """

        canonical_url = os.path.join(self._site_url, self._file_url)
        return canonical_url
