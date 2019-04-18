""" HTML Enhancer : get instances of HTML enhancements. """

from .canonical_url_creator import CanonicalURLCreator

class HTMLEnhancer():
    """ HTML Enhancer : get instances of HTML enhancements. """

    def __init__(self, article):
        _settings = getattr(article, 'settings', None)
        _file_url = getattr(article, 'url', None)

        self.canonical_link = CanonicalURLCreator(
            site_url=_settings.get('SITEURL'),
            file_url=_file_url,
        )
