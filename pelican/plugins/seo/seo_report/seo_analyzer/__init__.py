""" Launch micro SEO analysis. """

from .page_title_analyzer import PageTitleAnalyzer
from .page_description_analyzer import PageDescriptionAnalyzer
from .content_title_analyzer import ContentTitleAnalyzer
from .internal_link_analyzer import InternalLinkAnalyzer


class SEOAnalyzer():
    """ Instancy all micro SEO analyzers. """

    def __init__(self, article):
        self._title = getattr(article, 'title', None)
        self._description = getattr(article, 'description', None)
        self._content = getattr(article, 'content', None)
        self._settings = getattr(article, 'settings', None)

        self.page_title_analysis = PageTitleAnalyzer(title=self._title)
        self.page_description_analysis = PageDescriptionAnalyzer(
            description=self._description
        )
        self.content_title_analysis = ContentTitleAnalyzer(content=self._content)
        self.internal_link_analysis = InternalLinkAnalyzer(
            content=self._content,
            siteurl=self._settings['SITEURL']
        )
