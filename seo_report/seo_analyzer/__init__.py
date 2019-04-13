""" Launch micro SEO analysis. """

from .page_title_analyzer import PageTitleAnalyzer
from .page_description_analyzer import PageDescriptionAnalyzer
from .content_title_analyzer import ContentTitleAnalyzer
from .internal_link_analyzer import InternalLinkAnalyzer


class SEOAnalyzer():
    """ Instancy all micro SEO analyzers. """

    def __init__(self, article):
        self.page_title_analysis = PageTitleAnalyzer(article)
        self.page_description_analysis = PageDescriptionAnalyzer(article)
        self.content_title_analysis = ContentTitleAnalyzer(article)
        self.internal_link_analysis = InternalLinkAnalyzer(article)
