"""Unit tests for SEO Report."""

from unittest.mock import mock_open, patch

import pytest

from seo.seo_report.seo_analyzer import (
    ContentTitleAnalyzer,
    InternalLinkAnalyzer,
    PageDescriptionAnalyzer,
    PageTitleAnalyzer,
)


@pytest.fixture()
def seo_report(fake_seo_report, fake_articles_analysis):
    """
    Generates SEO report and returns its content.
    Need mock_open to do it.
    """

    with patch("seo.seo_report.open", mock_open()) as mocked_open:
        # Get a reference to the MagicMock that will be returned
        # when mock_open will be called
        # => When we do open("seo_report", "w") as report in generate, report
        # will also be a reference to the same MagicMock
        mocked_file_handle = mocked_open.return_value

        # When generate is executed, mock_open() is call instead of open()
        fake_seo_report.generate("Fake site", fake_articles_analysis)

        # mocked_open and the file handle got all
        # executed calls, and can assert them
        mocked_open.assert_called_once_with("seo_report.html", "w", encoding="utf8")
        mocked_file_handle.write.assert_called_once()

        # Get all arguments in the mocked write call and select the first
        # true arg (output)
        args, _ = mocked_file_handle.write.call_args_list[0]

        return args[0]


class TestSEOReport:
    """Units tests for SEOReport."""

    def test_launch_analysis_returns_dict(self, fake_article, fake_seo_report):
        """Test if launch_analysis return a dict with expected keys."""

        fake_articles_analysis = fake_seo_report.launch_analysis(fake_article)

        assert fake_articles_analysis["url"]
        assert fake_articles_analysis["date"]
        assert fake_articles_analysis["seo_analysis"]
        assert fake_articles_analysis["seo_analysis"]["page_title_analysis"]
        assert fake_articles_analysis["seo_analysis"]["page_description_analysis"]
        assert fake_articles_analysis["seo_analysis"]["content_title_analysis"]
        assert fake_articles_analysis["seo_analysis"]["internal_link_analysis"]

    def test_launch_analysis_values_are_instances_of_expected_analysis_objects(
        self, fake_article, fake_seo_report
    ):
        """
        Test if the dict returned by launch_analysis
        contained expected analysis objects.
        """

        fake_articles_analysis = fake_seo_report.launch_analysis(fake_article)
        fake_seo_analysis = fake_articles_analysis["seo_analysis"]

        page_title_analysis = fake_seo_analysis["page_title_analysis"]
        page_description_analysis = fake_seo_analysis["page_description_analysis"]
        content_title_analysis = fake_seo_analysis["content_title_analysis"]
        internal_link_analysis = fake_seo_analysis["internal_link_analysis"]

        assert isinstance(page_title_analysis, PageTitleAnalyzer)
        assert isinstance(page_description_analysis, PageDescriptionAnalyzer)
        assert isinstance(content_title_analysis, ContentTitleAnalyzer)
        assert isinstance(internal_link_analysis, InternalLinkAnalyzer)

    def test_generate_create_report_file_and_write_output(self, seo_report):
        """
        Test that generate create a HTML file and write SEO report on it.
        """

        assert "<h1>SEO report - Fake site</h1>" in seo_report

    def test_report_contains_correct_analysis(self, seo_report):
        """
        Test that generated HTML SEO report contains expected analysis.
        """

        # title
        # 3 out of 3 articles have included a title
        assert seo_report.count("You have declared a title. Nice job!") == 3
        # 1 out of 3 articles has a correct title
        assert seo_report.count("Your title has a good length.") == 1
        # 2 out of 3 articles have a title that is too short
        assert (
            seo_report.count(
                "Your title is too short. The recommended length is 70 characters."
            )
            == 2
        )

        # description
        # 2 out of 3 articles have included a description
        assert seo_report.count("You have declared a description. Nice job!") == 2
        # 1 out of 3 articles has a correct description
        assert seo_report.count("Your description has a good length.") == 1
        # 1 out of 3 articles have a title that is too short
        assert (
            seo_report.count(
                "Your description is too short. The minimum recommended length is 150 characters."
            )
            == 1
        )
        # 1 out of 3 articles is missing a description
        assert (
            seo_report.count("You need to declare a description to improve SEO.") == 1
        )

        # content title
        # 2 out of 3 articles have included a content title
        assert seo_report.count("You have declared a content title. Nice job!") == 2
        # 1 out of 3 articles has a non-unique content title
        assert seo_report.count("Your content title must be unique.") == 1
        # 1 out of 3 articles is missing the content title
        assert seo_report.count("You're missing a content title.") == 1

        # internal links
        # 2 out of 3 articles have 2 internal links
        assert seo_report.count("You've included 2 internal links. Nice job!") == 2
        # 1 out of 3 articles is missing internal links
        assert seo_report.count("It's better to include internal links.") == 1
