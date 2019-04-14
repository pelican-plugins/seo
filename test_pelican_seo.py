""" Units tests for Pelican SEO plugin. """

from unittest.mock import mock_open, patch

from .data_tests import (
    fake_article,
    fake_seo_report,
    fake_article_missing_elements,
    fake_article_multiple_elements,
    fake_articles_analysis,
    fake_seo_enhancer,
    fake_robots_rules,
)
from .seo_report.seo_analyzer import (
    InternalLinkAnalyzer,
    ContentTitleAnalyzer,
    PageTitleAnalyzer,
    PageDescriptionAnalyzer,
)
from .seo_enhancer.robots_file_creator import RobotsFileCreator

class TestSEOReport():
    """ Units tests for SEOReport. """

    def test_launch_analysis_returns_dict(self, fake_article, fake_seo_report):
        """ Test if launch_analysis return a dict with expected keys. """

        fake_articles_analysis = fake_seo_report.launch_analysis(fake_article)

        assert fake_articles_analysis['url']
        assert fake_articles_analysis['date']
        assert fake_articles_analysis['seo_analysis']
        assert fake_articles_analysis['seo_analysis']['page_title_analysis']
        assert fake_articles_analysis['seo_analysis']['page_description_analysis']
        assert fake_articles_analysis['seo_analysis']['content_title_analysis']
        assert fake_articles_analysis['seo_analysis']['internal_link_analysis']

    def test_launch_analysis_values_are_instances_of_expected_analysis_objects(self, fake_article, fake_seo_report):
        """ Test if the dict returned by launch_analysis contained expected analysis objects. """

        fake_articles_analysis = fake_seo_report.launch_analysis(fake_article)

        page_title_analysis = fake_articles_analysis['seo_analysis']['page_title_analysis']
        page_description_analysis = fake_articles_analysis['seo_analysis']['page_description_analysis']
        content_title_analysis = fake_articles_analysis['seo_analysis']['content_title_analysis']
        internal_link_analysis = fake_articles_analysis['seo_analysis']['internal_link_analysis']

        assert isinstance(page_title_analysis, PageTitleAnalyzer)
        assert isinstance(page_description_analysis, PageDescriptionAnalyzer)
        assert isinstance(content_title_analysis, ContentTitleAnalyzer)
        assert isinstance(internal_link_analysis, InternalLinkAnalyzer)

    def test_generate_create_report_file_and_write_output(self, fake_seo_report, fake_articles_analysis):
        """
        Test that generate create a HTML file and write SEO report on it.
        Need mock_open to test this.
        """

        with patch('pelican_seo.seo_report.open', mock_open()) as mocked_open:
            # Get a reference to the MagicMock that will be returned
            # when mock_open will be called
            # => When we do open("seo_report", "w") as report in generate, report
            # will also be a reference to the same MagicMock
            mocked_file_handle = mocked_open.return_value

            # When generate is executed, mock_open() is call instead of open()
            fake_seo_report.generate('Fake site', fake_articles_analysis)

            # mocked_open and the file handle got all executed calls, and can assert them
            mocked_open.assert_called_once_with('seo_report.html', 'w')
            mocked_file_handle.write.assert_called_once()

            # Get all arguments in the mocked write call and select the first
            # true arg (output)
            args, _ = mocked_file_handle.write.call_args_list[0]
            output = args[0]
            assert "<h1>SEO report - Fake site</h1>" in output


class TestPageTitleAnalyzer():
    """ Units tests for PageTitleAnalyzer. """

    def test_article_has_page_title(self, fake_article):
        """ Test if has_page_title returns True if fake_article has a title. """

        fake_analysis = PageTitleAnalyzer(fake_article)
        assert fake_analysis.has_page_title()

    def test_article_has_no_page_title(self, fake_article_missing_elements):
        """ Test if has_page_title returns False if fake_article has no title. """

        fake_analysis = PageTitleAnalyzer(fake_article_missing_elements)
        assert not fake_analysis.has_page_title()

    def test_article_page_title_length(self, fake_article):
        """ Test if page_title_length returns the good title length. """

        fake_analysis = PageTitleAnalyzer(fake_article)
        assert fake_analysis.page_title_length == len(fake_article.title)


class TestPageDescriptionAnalyzer():
    """ Units tests for PageDescriptionAnalyzer. """

    def test_article_has_page_description(self, fake_article):
        """ Test if has_page_description returns True if fake_article has a description. """

        fake_analysis = PageDescriptionAnalyzer(fake_article)
        assert fake_analysis.has_page_description()

    def test_article_has_no_page_description(self, fake_article_missing_elements):
        """ Test if has_page_description returns False if fake_article has no description. """

        fake_analysis = PageDescriptionAnalyzer(fake_article_missing_elements)
        assert not fake_analysis.has_page_description()

    def test_article_page_description_length(self, fake_article):
        """ Test if page_description_length returns the good description length. """

        fake_analysis = PageDescriptionAnalyzer(fake_article)
        assert fake_analysis.page_description_length == len(fake_article.description)


class TestContentTitleAnalyzer():
    """ Units tests for ContentTitleAnalyzer. """

    def test_article_has_content_title(self, fake_article):
        """ Test if has_content_title returns True if fake_article has a content title. """

        fake_analysis = ContentTitleAnalyzer(fake_article)
        assert fake_analysis.has_content_title()

    def test_article_has_no_content_title(self, fake_article_missing_elements):
        """ Test if has_content_title returns False if fake_article has no content title. """

        fake_analysis = ContentTitleAnalyzer(fake_article_missing_elements)
        assert not fake_analysis.has_content_title()

    def test_article_content_title_is_unique(self, fake_article):
        """ Test if is_content_title_unique returns True if content title is unique. """

        fake_analysis = ContentTitleAnalyzer(fake_article)
        assert fake_analysis.is_content_title_unique

    def test_article_content_title_is_not_unique(self, fake_article_multiple_elements):
        """ Test if is_content_title_unique returns False if content title is not unique. """

        fake_analysis = ContentTitleAnalyzer(fake_article_multiple_elements)
        assert not fake_analysis.is_content_title_unique()


class TestInternalLinkAnalyzer():
    """ Units tests for InternalLinkAnalyzer. """

    def test_article_has_internal_link(self, fake_article):
        """ Test if has_internal_link returns True if fake_article has at least one internal link. """

        fake_analysis = InternalLinkAnalyzer(fake_article)
        assert fake_analysis.has_internal_link()

    def test_article_has_no_internal_link(self, fake_article_missing_elements):
        """ Test if has_internal_link returns False if fake_article has no internal link. """

        fake_analysis = InternalLinkAnalyzer(fake_article_missing_elements)
        assert not fake_analysis.has_internal_link()

    def test_article_internal_link_occurrence(self, fake_article_multiple_elements):
        """ Test if internal_link_occurrence returns the rigth length. """

        fake_analysis = InternalLinkAnalyzer(fake_article_multiple_elements)
        assert fake_analysis.internal_link_occurrence == 2


class TestRobotsFileCreator():
    """ Units tests for RobotsFileCreator. """

    def test_get_all_robots_rules(self, fake_article):
        """ Test if get_noindex and get_disallow return True if the article has specific rules. """

        fake_robots = RobotsFileCreator(fake_article.metadata)
        assert fake_robots.get_noindex
        assert fake_robots.get_disallow
    
    def test_get_one_robots_rule(self, fake_article_missing_elements):
        """ Test if only get_noindex or get_disallow return True if the article has one specific rule. """

        fake_robots = RobotsFileCreator(fake_article_missing_elements.metadata)
        assert fake_robots.get_noindex
        assert not fake_robots.get_disallow

    def test_get_none_robots_rule(self, fake_article_multiple_elements):
        """ Test if get_noindex and get_disallow return None if the article has no specific rules. """

        fake_robots = RobotsFileCreator(fake_article_multiple_elements.metadata)
        assert not fake_robots.get_noindex
        assert not fake_robots.get_disallow

class TestSEOEnhancer():
    """ Units tests for SEOEnhancer. """

    def test_populate_robots_return_dict_with_rules_for_an_url(self, fake_seo_enhancer, fake_article):
        """
        Test that populate_robots return a dict with article_url,
        noindex and disallow rules.
        """

        fake_robots_rules = fake_seo_enhancer.populate_robots(fake_article)

        assert fake_robots_rules['article_url']
        assert fake_robots_rules['noindex']
        assert fake_robots_rules['disallow']

    def test_generate_robots_file(self, fake_seo_enhancer, fake_robots_rules):
        """ Test if generate_robots create a robots.txt file by mocking open(). """

        with patch('pelican_seo.seo_enhancer.open', mock_open()) as mocked_open:
            mocked_file_handle = mocked_open.return_value

            fake_seo_enhancer.generate_robots(fake_robots_rules)
            mocked_open.assert_called_once_with('output/robots.txt', 'w')
            mocked_file_handle.write.assert_called()
            # 4 : 1 fix write + 3 generated write
            assert len(mocked_file_handle.write.call_args_list) == 4

            args, _ = mocked_file_handle.write.call_args_list[1]
            fake_rule = args[0]
            assert "Noindex: fake-title.html" in fake_rule
