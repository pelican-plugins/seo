""" Launch micro SEO analysis. """

from .page_title_analyzer import PageTitleAnalyzer
from .page_description_analyzer import PageDescriptionAnalyzer
from .content_title_analyzer import ContentTitleAnalyzer


class SEOAnalyzer():
    """ Instancy all micro SEO analyzers. """

    def __init__(self, article):
        self.page_title_analysis = PageTitleAnalyzer(article)
        self.page_description_analysis = PageDescriptionAnalyzer(article)
        self.content_title_analysis = ContentTitleAnalyzer(article)
