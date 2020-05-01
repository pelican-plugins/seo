""" Units tests for Canonical URL Creator. """

from seo.seo_enhancer.html_enhancer import CanonicalURLCreator


class TestCanonicalURLCreator():
    """ Unit tests for CanonicalURLCreator. """

    def test_create_url(self, fake_article):
        """ Test if create_url() returns the join of site URL and article URL. """

        canonical = CanonicalURLCreator(
            fileurl=fake_article.url,
            siteurl=fake_article.settings['SITEURL']
        )
        canonical_link = canonical.create_url()

        assert canonical_link == "fakesite.com/fake-title.html"
