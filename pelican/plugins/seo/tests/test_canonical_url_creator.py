""" Units tests for Canonical URL Creator. """

from seo.seo_enhancer.html_enhancer import CanonicalURLCreator


class TestCanonicalURLCreator:
    """ Unit tests for CanonicalURLCreator. """

    def test_create_url(self, fake_article):
        """ Test if create_url() returns the join of site URL and article URL. """

        canonical = CanonicalURLCreator(
            fileurl=fake_article.url, siteurl=fake_article.settings["SITEURL"]
        )
        canonical_link = canonical.create_url()

        assert canonical_link == "fakesite.com/fake-title.html"

    def test_create_url_with_save_as_metadata(self, fake_seo_enhancer, fake_article):
        """ Test that canonical URL is build with save_as metadata when filled. """

        fake_article.metadata["save_as"] = "custom_file_name.html"

        html_enhancements = fake_seo_enhancer.launch_html_enhancer(
            file=fake_article,
            output_path="fake_output",
            path="fake_output/fake_file.html",
        )

        assert (
            html_enhancements["canonical_tag"] == "fakesite.com/custom_file_name.html"
        )
