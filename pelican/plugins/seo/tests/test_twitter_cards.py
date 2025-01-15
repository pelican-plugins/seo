"""Units tests for Twitter Cards."""

from seo.seo_enhancer.html_enhancer import TwitterCards


class TestTwitterCards:
    """Unit tests for Twitter Cards."""

    def test_create_tags(self, fake_article):
        """
        Test that create_tags() returns all Twitter Cards tags
        if all elements are filled.
        """

        tw = TwitterCards(
            tw_account=fake_article.metadata["tw_account"],
        )

        tw_tags = tw.create_tags()

        assert tw_tags["card"] == "summary"
        assert tw_tags["site"] == "@TestTWCards"

    def test_create_tags_missing_elements(self, fake_article_missing_elements):
        """
        Test that create_tags() without specific elements
        doesn't return them.
        """

        tw = TwitterCards(
            tw_account=fake_article_missing_elements.metadata["tw_account"],
        )

        tw_tags = tw.create_tags()

        assert "site" not in tw_tags
        assert tw_tags["card"] == "summary"
