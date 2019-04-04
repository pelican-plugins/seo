""" Units tests for Pelican SEO plugin. """

from .data_tests import (
    fake_article,
    fake_seo_report,
    fake_article_missing_elements,
    fake_article_multiple_elements
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

    def test_has_no_page_title(self, fake_article_missing_elements):
        """ Test if has_page_title returns False if fake_article has no title. """

        fake_analysis = PageTitleAnalyzer(fake_article_missing_elements)
        assert not fake_analysis.has_page_title()

    def test_page_title_length(self, fake_article):
        """ Test if page_title_length returns the good title length. """

        fake_analysis = PageTitleAnalyzer(fake_article)
        assert fake_analysis.page_title_length == len(fake_article.title)


class TestPageDescriptionAnalyzer():
    """ Units tests for PageDescriptionAnalyzer. """

    def test_has_page_description(self, fake_article):
        """ Test if has_page_description returns True if fake_article has a description. """

        fake_analysis = PageDescriptionAnalyzer(fake_article)
        assert fake_analysis.has_page_description()

    def test_has_no_page_description(self, fake_article_missing_elements):
        """ Test if has_page_description returns False if fake_article has no description. """

        fake_analysis = PageDescriptionAnalyzer(fake_article_missing_elements)
        assert not fake_analysis.has_page_description()

    def test_page_description_length(self, fake_article):
        """ Test if page_description_length returns the good description length. """

        fake_analysis = PageDescriptionAnalyzer(fake_article)
        assert fake_analysis.page_description_length == len(fake_article.description)


class TestContentTitleAnalyzer():
    """ Units tests for ContentTitleAnalyzer. """

    def test_has_content_description(self, fake_article):
        """ Test if has_content_description returns True if fake_article has a content title. """

        fake_analysis = ContentTitleAnalyzer(fake_article)
        assert fake_analysis.has_content_title()

    def test_has_no_content_title(self, fake_article_missing_elements):
        """ Test if has_content_title returns False if fake_article has no content title. """

        fake_analysis = ContentTitleAnalyzer(fake_article_missing_elements)
        assert not fake_analysis.has_content_title()

    def test_content_title_is_unique(self, fake_article):
        """ Test if is_content_title_unique returns True if content title is unique. """

        fake_analysis = ContentTitleAnalyzer(fake_article)
        assert fake_analysis.is_content_title_unique

    def test_content_title_is_not_unique(self, fake_article_multiple_elements):
        """ Test if is_content_title_unique returns False if content title is not unique. """

        fake_analysis = ContentTitleAnalyzer(fake_article_multiple_elements)
        assert not fake_analysis.is_content_title_unique()


class TestInternalLinkAnalyzer():
    """ Units tests for InternalLinkAnalyzer. """

    def test_has_internal_link(self, fake_article):
        """ Test if has_internal_link returns True if fake_article has at least one internal link. """

        fake_analysis = InternalLinkAnalyzer(fake_article)
        assert fake_analysis.has_internal_link()

    def test_has_no_internal_link(self, fake_article_missing_elements):
        """ Test if has_internal_link returns False if fake_article has no internal link. """

        fake_analysis = InternalLinkAnalyzer(fake_article_missing_elements)
        assert not fake_analysis.has_internal_link()

    def test_internal_link_occurrence(self, fake_article_multiple_elements):
        """ Test if internal_link_occurrence returns the rigth length. """

        fake_analysis = InternalLinkAnalyzer(fake_article_multiple_elements)
        assert fake_analysis.internal_link_occurrence == 2
