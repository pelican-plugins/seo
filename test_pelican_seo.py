""" Units tests for Pelican SEO plugin. """

from .data_tests import (
    fake_article,
    fake_seo_report,
)
from .seo_report.seo_analyzer import (
    InternalLinkAnalyzer,
    ContentTitleAnalyzer,
    PageTitleAnalyzer,
    PageDescriptionAnalyzer,
)


class TestSEOReport():
    """ Units tests for SEOReport object. """

    def test_launch_analysis_returns_dict(self, fake_article, fake_seo_report):
        """ Test if launch_analysis return a dict with expected keys. """

        fake_articles_analysis = fake_seo_report.launch_analysis(fake_article)

        assert fake_articles_analysis['url']
        assert fake_articles_analysis['date']
        assert fake_articles_analysis['seo_analysis']
        assert fake_articles_analysis['seo_analysis']['page_title_analysis']
        assert fake_articles_analysis['seo_analysis']['page_description_analysis']
        assert fake_articles_analysis['seo_analysis']['content_title_analysis']
        assert fake_articles_analysis['seo_analysis']['internal_link_analysis']

    def test_launch_analysis_values_are_instances_of_expected_analysis_objects(self, fake_article, fake_seo_report):
        """ Test if the dict returned by launch_analysis contained expected analysis objects. """

        fake_articles_analysis = fake_seo_report.launch_analysis(fake_article)

        page_title_analysis = fake_articles_analysis['seo_analysis']['page_title_analysis']
        page_description_analysis = fake_articles_analysis['seo_analysis']['page_description_analysis']
        content_title_analysis = fake_articles_analysis['seo_analysis']['content_title_analysis']
        internal_link_analysis = fake_articles_analysis['seo_analysis']['internal_link_analysis']

        assert isinstance(page_title_analysis, PageTitleAnalyzer)
        assert isinstance(page_description_analysis, PageDescriptionAnalyzer)
        assert isinstance(content_title_analysis, ContentTitleAnalyzer)
        assert isinstance(internal_link_analysis, InternalLinkAnalyzer)

    def test_generate_report(self):
        """  """

        pass


class TestPageTitleAnalyzer():
    """ Units tests for PageTitleAnalyze. """

    def test_has_page_title(self, fake_article):
        """ Test if has_page_title returns True if fake_article has a title. """

        fake_analysis = PageTitleAnalyzer(fake_article)
        assert fake_analysis.has_page_title()

    def test_page_title_length(self, fake_article):
        """ Test if page_title_length returns the good title length. """

        fake_analysis = PageTitleAnalyzer(fake_article)
        assert fake_analysis.page_title_length == len(fake_article.title)
