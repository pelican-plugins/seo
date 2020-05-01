""" Unit tests for Internal Link Analyzer. """

from seo.seo_report.seo_analyzer import InternalLinkAnalyzer


class TestInternalLinkAnalyzer():
    """ Units tests for InternalLinkAnalyzer. """

    def test_article_has_internal_link(self, fake_article):
        """
        Test if has_internal_link returns True
        if fake_article has at least one internal link.
        """

        fake_analysis = InternalLinkAnalyzer(
            content=fake_article.content,
            siteurl=fake_article.settings['SITEURL'],
        )
        assert fake_analysis.has_internal_link()

    def test_article_has_no_internal_link(self, fake_article_missing_elements):
        """
        Test if has_internal_link returns False
        if fake_article has no internal link.
        """

        fake_analysis = InternalLinkAnalyzer(
            content=fake_article_missing_elements.content,
            siteurl=fake_article_missing_elements.settings['SITEURL'],
        )
        assert not fake_analysis.has_internal_link()

    def test_article_internal_link_occurrence(self, fake_article_multiple_elements):
        """ Test if internal_link_occurrence returns the rigth length. """

        fake_analysis = InternalLinkAnalyzer(
            content=fake_article_multiple_elements.content,
            siteurl=fake_article_multiple_elements.settings['SITEURL'],
        )
        assert fake_analysis.internal_link_occurrence == 2
