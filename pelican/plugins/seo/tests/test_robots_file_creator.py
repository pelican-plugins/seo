""" Units tests for Robots File Creator. """

from seo.seo_enhancer.robots_file_creator import RobotsFileCreator


class TestRobotsFileCreator():
    """ Units tests for RobotsFileCreator. """

    def test_get_all_robots_rules(self, fake_article):
        """
        Test if get_noindex and get_disallow return True
        if the article has specific rules.
        """

        fake_robots = RobotsFileCreator(fake_article.metadata)
        assert fake_robots.get_noindex
        assert fake_robots.get_disallow

    def test_get_one_robots_rule(self, fake_article_missing_elements):
        """
        Test if only get_noindex or get_disallow return True
        if the article has one specific rule.
        """

        fake_robots = RobotsFileCreator(fake_article_missing_elements.metadata)
        assert fake_robots.get_noindex
        assert not fake_robots.get_disallow

    def test_get_none_robots_rule(self, fake_article_multiple_elements):
        """
        Test if get_noindex and get_disallow return None
        if the article has no specific rules.
        """

        fake_robots = RobotsFileCreator(fake_article_multiple_elements.metadata)
        assert not fake_robots.get_noindex
        assert not fake_robots.get_disallow
