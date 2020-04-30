""" Unit tests for Page Title Analyzer. """

from seo.seo_report.seo_analyzer import PageTitleAnalyzer


class TestPageTitleAnalyzer():
    """ Units tests for PageTitleAnalyzer. """

    def test_article_has_page_title(self, fake_article):
        """ Test if has_page_title returns True if fake_article has a title. """

        fake_analysis = PageTitleAnalyzer(title=fake_article.title)
        assert fake_analysis.has_page_title()

    def test_article_has_no_page_title(self, fake_article_missing_elements):
        """ Test if has_page_title returns False if fake_article has no title. """

        fake_analysis = PageTitleAnalyzer(title=fake_article_missing_elements.title)
        assert not fake_analysis.has_page_title()

    def test_article_page_title_length(self, fake_article):
        """ Test if page_title_length returns the good title length. """

        fake_analysis = PageTitleAnalyzer(title=fake_article.title)
        assert fake_analysis.page_title_length == len(fake_article.title)
