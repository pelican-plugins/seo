"""Units tests for OpenGraph."""

import locale

import pytest

from seo.seo_enhancer.html_enhancer import OpenGraph


class TestOpenGraph:
    """Unit tests for OpenGraph."""

    def test_create_absolute_fileurl(self, fake_article):
        """
        Test if create_absolute_fileurl() returns the join
        of site URL and file URL.
        """

        og = OpenGraph(
            siteurl=fake_article.settings["SITEURL"],
            fileurl=fake_article.url,
            file_type=None,
            title=None,
            description=None,
            image=None,
            locale=None,
        )
        fileurl = og._create_absolute_fileurl()

        assert fileurl == "https://www.fakesite.com/fake-title.html"

    @pytest.mark.parametrize(
        "locale,expected_result",
        [
            (["fr_FR", "en_US"], "fr_FR"),
            (["en_US", "fr_FR"], "en_US"),
            ([""], locale.getdefaultlocale()[0]),
        ],
    )
    def test_get_locale(self, locale, expected_result):
        """
        Test that _get_locale() returns:
        - either the first value of LOCALE Pelican setting if filled
        - or the language from the default system locale.
        """

        og = OpenGraph(
            siteurl=None,
            fileurl=None,
            file_type=None,
            title=None,
            description=None,
            image=None,
            locale=locale,
        )
        language = og._get_locale()

        assert language == expected_result

    def test_create_tags(self, fake_article):
        """
        Test that create_tags() returns all OG tags
        if all elements are filled.
        """

        og = OpenGraph(
            siteurl=fake_article.settings["SITEURL"],
            fileurl=fake_article.url,
            file_type="article",
            title=fake_article.metadata["og_title"],
            description=fake_article.metadata["og_description"],
            image=fake_article.metadata["og_image"],
            locale=fake_article.settings["LOCALE"],
        )

        og_tags = og.create_tags()

        assert og_tags["url"] == "https://www.fakesite.com/fake-title.html"
        assert og_tags["type"] == "article"
        assert og_tags["title"] == "OG Title"
        assert og_tags["description"] == "OG Description"
        assert og_tags["image"] == "https://www.fakesite.com/og-image.jpg"
        assert og_tags["locale"] == "fr_FR"

    def test_create_tags_missing_elements(self, fake_article_missing_elements):
        """
        Test that create_tags() without specific elements
        doesn't return them.
        """

        og = OpenGraph(
            siteurl=fake_article_missing_elements.settings["SITEURL"],
            fileurl=fake_article_missing_elements.url,
            file_type="article",
            title=fake_article_missing_elements.title,
            description=fake_article_missing_elements.description,
            image=fake_article_missing_elements.metadata["image"],
            locale="fr_FR",
        )

        og_tags = og.create_tags()

        assert "title" not in og_tags
        assert "description" not in og_tags
        assert "image" not in og_tags
