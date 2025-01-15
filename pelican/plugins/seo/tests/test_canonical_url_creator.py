"""Units tests for Canonical URL Creator."""

import pytest

from seo.seo_enhancer.html_enhancer import CanonicalURLCreator


class TestCanonicalURLCreator:
    """Unit tests for CanonicalURLCreator."""

    def test_create_url(self, fake_article):
        """Test if create_url() returns the join of site URL and article URL."""

        canonical = CanonicalURLCreator(
            fileurl=fake_article.url, siteurl=fake_article.settings["SITEURL"]
        )
        canonical_link = canonical.create_url()

        assert canonical_link == "https://www.fakesite.com/fake-title.html"

    @pytest.mark.parametrize(
        "metadata,value,expected",
        [
            (
                "save_as",
                "custom_file_name.html",
                "https://www.fakesite.com/custom_file_name.html",
            ),
            (
                "external_canonical",
                "https://www.example.com/external_canonical_article.html",
                "https://www.example.com/external_canonical_article.html",
            ),
        ],
    )
    def test_create_url_with_save_as_or_external_canonical_metadata(
        self, fake_seo_enhancer, fake_article, metadata, value, expected
    ):
        """
        Test that canonical URL is correctly built with:
        - :save_as: metadata filled
        - :external_canonical: metadata filled
        """

        fake_article.metadata[metadata] = value

        html_enhancements = fake_seo_enhancer.launch_html_enhancer(
            file=fake_article,
            output_path="fake_output",
            path="fake_output/fake_file.html",
        )

        assert html_enhancements["canonical_tag"] == expected

    def test_create_url_with_external_canonical_and_save_as_metadata(
        self, fake_seo_enhancer, fake_article
    ):
        """Test that canonical URL is build with :external_canonical: metadata value, even when :save_as: metadata is filled."""

        fake_article.metadata["external_canonical"] = (
            "https://www.example.com/external_canonical_article.html"
        )
        fake_article.metadata["save_as"] = "custom_file_name.html"

        html_enhancements = fake_seo_enhancer.launch_html_enhancer(
            file=fake_article,
            output_path="fake_output",
            path="fake_output/fake_file.html",
        )

        assert (
            html_enhancements["canonical_tag"]
            == "https://www.example.com/external_canonical_article.html"
        )
