"""Units tests for Breadcrumb Schema Creator."""

import pytest

from seo.seo_enhancer.html_enhancer import BreadcrumbSchemaCreator


class TestBreadcrumbSchemaCreator:
    """Unit tests for BreadcrumbSchemaCreator."""

    def test_create_schema(self, fake_article):
        """
        Test that create_schema() returns a valid
        schema.org (dict) for breadcrumb.
        """

        breadcrumb = BreadcrumbSchemaCreator(
            output_path="fake_output",
            path="fake_output/fake-file.html",
            sitename=fake_article.settings["SITENAME"],
            siteurl=fake_article.settings["SITEURL"],
        )

        fake_breadcrumb_schema = breadcrumb.create_schema()

        assert fake_breadcrumb_schema["@context"] == "https://schema.org"
        assert fake_breadcrumb_schema["@type"] == "BreadcrumbList"

        assert len(fake_breadcrumb_schema["itemListElement"]) == 2

        assert fake_breadcrumb_schema["itemListElement"][0]["@type"] == "ListItem"
        assert fake_breadcrumb_schema["itemListElement"][0]["position"] == 1
        assert fake_breadcrumb_schema["itemListElement"][0]["name"] == "Fake Site Name"
        assert (
            fake_breadcrumb_schema["itemListElement"][0]["item"]
            == "https://www.fakesite.com"
        )

        assert fake_breadcrumb_schema["itemListElement"][1]["@type"] == "ListItem"
        assert fake_breadcrumb_schema["itemListElement"][1]["position"] == 2
        assert fake_breadcrumb_schema["itemListElement"][1]["name"] == "Fake file"
        assert (
            fake_breadcrumb_schema["itemListElement"][1]["item"]
            == "https://www.fakesite.com/fake-file.html"
        )

    @pytest.mark.parametrize(
        "output_path,path",
        [
            (
                "fake_output",
                "fake_output/test/blabla/other/kiwi/fake-file.html",
            ),
            (
                "/home/kiwi/pelican/my-site/fake_output",
                "/home/kiwi/pelican/my-site/fake_output/test/blabla/other/kiwi/fake-file.html",
            ),
        ],
    )
    def test_create_schema_with_x_elements_in_path(
        self, fake_article, output_path, path
    ):
        """
        Test that create_schema returns a valid schema.org (dict)
        for an absolute or relative path with x elements.
        """

        breadcrumb = BreadcrumbSchemaCreator(
            output_path=output_path,
            path=path,
            sitename=fake_article.settings["SITENAME"],
            siteurl=fake_article.settings["SITEURL"],
        )

        fake_breadcrumb_schema = breadcrumb.create_schema()

        assert len(fake_breadcrumb_schema["itemListElement"]) == 6

    def test_create_schema_with_no_sitename_no_siteurl(self, fake_article):
        """Test that create_schema returns incomplete schema.org."""

        breadcrumb = BreadcrumbSchemaCreator(
            output_path="fake_output",
            path="fake_output/fake-file.html",
            sitename="",
            siteurl="",
        )

        fake_breadcrumb_schema = breadcrumb.create_schema()

        assert not fake_breadcrumb_schema["itemListElement"][0]["position"] == 1

    def test_create_schema_with_no_sitename(self, fake_article):
        """
        Test that create_schema with siteurl but no
        sitename returns incomplete schema.org.
        """

        breadcrumb = BreadcrumbSchemaCreator(
            output_path="fake_output",
            path="fake_output/fake-file.html",
            sitename="",
            siteurl=fake_article.settings["SITEURL"],
        )

        fake_breadcrumb_schema = breadcrumb.create_schema()

        assert not fake_breadcrumb_schema["itemListElement"][0]["position"] == 1

    def test_create_schema_with_no_siteurl(self, fake_article):
        """
        Test that create_schema with sitename but no
        siteurl returns incomplete schema.org.
        """

        breadcrumb = BreadcrumbSchemaCreator(
            output_path="fake_output",
            path="fake_output/fake-file.html",
            sitename=fake_article.settings["SITENAME"],
            siteurl="",
        )

        fake_breadcrumb_schema = breadcrumb.create_schema()

        assert not fake_breadcrumb_schema["itemListElement"][0]["position"] == 1
