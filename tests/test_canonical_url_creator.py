""" Units tests for Canonical URL Creator. """

from ave_seo.seo_enhancer.html_enhancer import CanonicalURLCreator
from .data_tests import (
    fake_article,
)


class TestCanonicalURLCreator():
    """ Unit tests for CanonicalURLCreator. """

    def test_create_url(self, fake_article):
        """ Test if create_url() returns the join of site URL and article URL. """

        canonical = CanonicalURLCreator(fake_article.url, fake_article.settings['SITEURL'])
        canonical_link = canonical.create_url()

        assert canonical_link == "fakesite.com/fake-title.html"
