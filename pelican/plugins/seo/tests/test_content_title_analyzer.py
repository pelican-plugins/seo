""" Unit tests for Content Title Analyzer. """

from seo.seo_report.seo_analyzer import ContentTitleAnalyzer


class TestContentTitleAnalyzer():
    """ Units tests for ContentTitleAnalyzer. """

    def test_article_has_content_title(self, fake_article):
        """
        Test if has_content_title returns True
        if fake_article has a content title.
        """

        fake_analysis = ContentTitleAnalyzer(content=fake_article.content)
        assert fake_analysis.has_content_title()

    def test_article_has_no_content_title(self, fake_article_missing_elements):
        """
        Test if has_content_title returns False
        if fake_article has no content title.
        """

        fake_analysis = ContentTitleAnalyzer(
            content=fake_article_missing_elements.content
        )
        assert not fake_analysis.has_content_title()

    def test_article_content_title_is_unique(self, fake_article):
        """ Test if is_content_title_unique returns True if content title is unique. """

        fake_analysis = ContentTitleAnalyzer(content=fake_article.content)
        assert fake_analysis.is_content_title_unique

    def test_article_content_title_is_not_unique(self, fake_article_multiple_elements):
        """
        Test if is_content_title_unique returns False
        if content title is not unique.
        """

        fake_analysis = ContentTitleAnalyzer(
            content=fake_article_multiple_elements.content
        )
        assert not fake_analysis.is_content_title_unique()
