""" Unit tests for Page Description Analyzer. """

from seo.seo_report.seo_analyzer import PageDescriptionAnalyzer


class TestPageDescriptionAnalyzer():
    """ Units tests for PageDescriptionAnalyzer. """

    def test_article_has_page_description(self, fake_article):
        """
        Test if has_page_description returns True
        if fake_article has a description.
        """

        fake_analysis = PageDescriptionAnalyzer(description=fake_article.description)
        assert fake_analysis.has_page_description()

    def test_article_has_no_page_description(self, fake_article_missing_elements):
        """
        Test if has_page_description returns False
        if fake_article has no description.
        """

        fake_analysis = PageDescriptionAnalyzer(
            description=fake_article_missing_elements.description
        )
        assert not fake_analysis.has_page_description()

    def test_article_page_description_length(self, fake_article):
        """
        Test if page_description_length returns
        the good description length.
        """

        fake_analysis = PageDescriptionAnalyzer(description=fake_article.description)
        assert fake_analysis.page_description_length == len(fake_article.description)
