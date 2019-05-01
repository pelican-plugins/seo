""" Units tests for Pelican SEO plugin. """

from unittest.mock import mock_open, patch

from ave_seo.seo_report.seo_analyzer import (
    InternalLinkAnalyzer,
    ContentTitleAnalyzer,
    PageTitleAnalyzer,
    PageDescriptionAnalyzer,
)
from ave_seo.seo_enhancer.robots_file_creator import RobotsFileCreator
from ave_seo.seo_enhancer.html_enhancer import (
    CanonicalURLCreator,
    ArticleSchemaCreator,
    BreadcrumbSchemaCreator,
)
from .data_tests import (
    fake_article,
    fake_seo_report,
    fake_article_missing_elements,
    fake_article_multiple_elements,
    fake_articles_analysis,
    fake_seo_enhancer,
    fake_robots_rules,
)


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

        with patch('ave_seo.seo_report.open', mock_open()) as mocked_open:
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

        with patch('ave_seo.seo_enhancer.open', mock_open()) as mocked_open:
            mocked_file_handle = mocked_open.return_value

            fake_seo_enhancer.generate_robots(fake_robots_rules)
            mocked_open.assert_called_once_with('output/robots.txt', 'w')
            mocked_file_handle.write.assert_called()
            # 4 : 1 fix write + 3 generated write
            assert len(mocked_file_handle.write.call_args_list) == 4

            args, _ = mocked_file_handle.write.call_args_list[1]
            fake_rule = args[0]
            assert "Noindex: fake-title.html" in fake_rule

    def test_launch_html_enhancemer_returns_dict(self, fake_article, fake_seo_enhancer):
        """ Test if launch_html_enhancemer returns a dict with expected keys. """

        fake_html_enhancements = fake_seo_enhancer.launch_html_enhancer(
            article=fake_article,
            output_path='fake_output',
            path='fake_dir/fake_output/fake_file.html',
        )

        assert fake_html_enhancements['canonical_tag']
        assert fake_html_enhancements['article_schema']
        assert fake_html_enhancements['breadcrumb_schema']

    def test_add_html_enhancements_to_file(self, fake_article, fake_seo_enhancer):
        """ Test if add_html_to_file add SEO enhancements to HTML files by mocking open(). """

        path = "fake_dir/fake_output/fake_file.html"
        fake_html_enhancements = fake_seo_enhancer.launch_html_enhancer(
            article=fake_article,
            output_path='fake_output',
            path=path,
        )

        with patch('ave_seo.seo_enhancer.open', mock_open(read_data=fake_article.content)) as mocked_open:
            mocked_file_handle = mocked_open.return_value

            fake_seo_enhancer.add_html_to_file(fake_html_enhancements, path)
            assert len(mocked_open.call_args_list) == 2
            mocked_file_handle.read.assert_called_once()
            mocked_file_handle.write.assert_called_once()

            write_args, _ = mocked_file_handle.write.call_args_list[0]
            fake_html_content = write_args[0]
            assert '<link href="fakesite.com/fake-title.html" rel="canonical"/>' in fake_html_content
            assert '{"@context": "https://schema.org", "@type": "Article"' in fake_html_content
            assert '{"@context": "https://schema.org", "@type": "BreadcrumbList"' in fake_html_content


class TestCanonicalURLCreator():
    """ Unit tests for CanonicalURLCreator. """

    def test_create_url(self, fake_article):
        """ Test if create_url() returns the join of site URL and article URL. """

        canonical = CanonicalURLCreator(fake_article.url, fake_article.settings['SITEURL'])
        canonical_link = canonical.create_url()

        assert canonical_link == "fakesite.com/fake-title.html"


class TestArticleSchemaCreator():
    """ Unit tests for ArticleSchemaCreator. """

    def test_create_schema(self, fake_article):
        """ Test that create_schema returns a valid schema.org (dict). """

        article = ArticleSchemaCreator(
            author=fake_article.author,
            title=fake_article.title,
            category=fake_article.category,
            date=fake_article.date,
            logo=fake_article.settings['LOGO'],
            image=fake_article.metadata['image'],
            sitename=fake_article.settings['SITENAME'],
        )

        fake_article_schema = article.create_schema()

        assert fake_article_schema['@context'] == "https://schema.org"
        assert fake_article_schema['@type'] == "Article"

        assert fake_article_schema['author']['@type'] == 'Person'
        assert fake_article_schema['author']['name'] == 'Fake author'

        assert fake_article_schema['publisher']['@type'] == 'Organization'
        assert fake_article_schema['publisher']['name'] == 'Fake Site Name'
        assert fake_article_schema['publisher']['logo']['@type'] == 'ImageObject'
        assert fake_article_schema['publisher']['logo']['url'] == 'https://www.fakesite.com/fake-logo.jpg'

        assert fake_article_schema['headline'] == 'Fake Title'

        assert fake_article_schema['about'] == 'Fake category'

        assert fake_article_schema['datePublished'] == '2019-04-03 23:49'

        assert fake_article_schema['image'] == 'https://www.fakesite.com/fake-image.jpg'

    def test_create_schema_with_incomplete_article(self, fake_article_missing_elements):
        """ Test that create_schema returns a schema.org, even if article is incomplete. """

        article = ArticleSchemaCreator(
            author=fake_article_missing_elements.author,
            title=fake_article_missing_elements.title,
            category=fake_article_missing_elements.category,
            date='',
            logo=fake_article_missing_elements.settings['LOGO'],
            image=fake_article_missing_elements.metadata['image'],
            sitename=fake_article_missing_elements.settings['SITENAME'],
        )

        fake_article_schema = article.create_schema()

        assert fake_article_schema['@context'] == "https://schema.org"
        assert fake_article_schema['@type'] == "Article"

        assert 'author' not in fake_article_schema
        assert 'publisher' not in fake_article_schema
        assert 'headline' not in fake_article_schema
        assert 'about' not in fake_article_schema
        assert 'datePublished' not in fake_article_schema
        assert 'image' not in fake_article_schema

    def test_create_schema_with_author_missing(self, fake_article, fake_article_missing_elements):
        """ Test that create_schema returns a schema.org, with author missing. """

        article = ArticleSchemaCreator(
            author=fake_article_missing_elements.author,
            title=fake_article.title,
            category=fake_article.category,
            date=fake_article.date,
            logo=fake_article.settings['LOGO'],
            image=fake_article.metadata['image'],
            sitename=fake_article.settings['SITENAME'],
        )

        fake_article_schema = article.create_schema()

        assert 'Fake author' not in fake_article_schema

        assert fake_article_schema['publisher']['name'] == 'Fake Site Name'
        assert fake_article_schema['publisher']['logo']['url'] == 'https://www.fakesite.com/fake-logo.jpg'
        assert fake_article_schema['headline'] == 'Fake Title'
        assert fake_article_schema['about'] == 'Fake category'
        assert fake_article_schema['datePublished'] == '2019-04-03 23:49'
        assert fake_article_schema['image'] == 'https://www.fakesite.com/fake-image.jpg'

    def test_create_schema_with_title_missing(self, fake_article, fake_article_missing_elements):
        """ Test that create_schema returns a schema.org, with title missing. """

        article = ArticleSchemaCreator(
            author=fake_article.author,
            title=fake_article_missing_elements.title,
            category=fake_article.category,
            date=fake_article.date,
            logo=fake_article.settings['LOGO'],
            image=fake_article.metadata['image'],
            sitename=fake_article.settings['SITENAME'],
        )

        fake_article_schema = article.create_schema()

        assert 'Fake Title' not in fake_article_schema

        assert fake_article_schema['author']['name'] == 'Fake author'
        assert fake_article_schema['publisher']['name'] == 'Fake Site Name'
        assert fake_article_schema['publisher']['logo']['url'] == 'https://www.fakesite.com/fake-logo.jpg'
        assert fake_article_schema['about'] == 'Fake category'
        assert fake_article_schema['datePublished'] == '2019-04-03 23:49'
        assert fake_article_schema['image'] == 'https://www.fakesite.com/fake-image.jpg'

    def test_create_schema_with_category_missing(self, fake_article, fake_article_missing_elements):
        """ Test that create_schema returns a schema.org, with category missing. """

        article = ArticleSchemaCreator(
            author=fake_article.author,
            title=fake_article.title,
            category=fake_article_missing_elements.category,
            date=fake_article.date,
            logo=fake_article.settings['LOGO'],
            image=fake_article.metadata['image'],
            sitename=fake_article.settings['SITENAME'],
        )

        fake_article_schema = article.create_schema()

        assert 'Fake category' not in fake_article_schema

        assert fake_article_schema['author']['name'] == 'Fake author'
        assert fake_article_schema['publisher']['name'] == 'Fake Site Name'
        assert fake_article_schema['publisher']['logo']['url'] == 'https://www.fakesite.com/fake-logo.jpg'
        assert fake_article_schema['headline'] == 'Fake Title'
        assert fake_article_schema['datePublished'] == '2019-04-03 23:49'
        assert fake_article_schema['image'] == 'https://www.fakesite.com/fake-image.jpg'

    def test_create_schema_with_date_missing(self, fake_article, fake_article_missing_elements):
        """ Test that create_schema returns a schema.org, with date missing. """

        article = ArticleSchemaCreator(
            author=fake_article.author,
            title=fake_article.title,
            category=fake_article.category,
            date='',
            logo=fake_article.settings['LOGO'],
            image=fake_article.metadata['image'],
            sitename=fake_article.settings['SITENAME'],
        )

        fake_article_schema = article.create_schema()

        assert '2019-04-03 23:49' not in fake_article_schema

        assert fake_article_schema['author']['name'] == 'Fake author'
        assert fake_article_schema['publisher']['name'] == 'Fake Site Name'
        assert fake_article_schema['publisher']['logo']['url'] == 'https://www.fakesite.com/fake-logo.jpg'
        assert fake_article_schema['headline'] == 'Fake Title'
        assert fake_article_schema['about'] == 'Fake category'
        assert fake_article_schema['image'] == 'https://www.fakesite.com/fake-image.jpg'

    def test_create_schema_with_logo_missing(self, fake_article, fake_article_missing_elements):
        """ Test that create_schema returns a schema.org, with logo missing. """

        article = ArticleSchemaCreator(
            author=fake_article.author,
            title=fake_article.title,
            category=fake_article.category,
            date=fake_article.date,
            logo=fake_article_missing_elements.settings['LOGO'],
            image=fake_article.metadata['image'],
            sitename=fake_article.settings['SITENAME'],
        )

        fake_article_schema = article.create_schema()

        assert 'https://www.fakesite.com/fake-logo.jpg' not in fake_article_schema

        assert fake_article_schema['author']['name'] == 'Fake author'
        assert fake_article_schema['publisher']['name'] == 'Fake Site Name'
        assert fake_article_schema['headline'] == 'Fake Title'
        assert fake_article_schema['about'] == 'Fake category'
        assert fake_article_schema['datePublished'] == '2019-04-03 23:49'
        assert fake_article_schema['image'] == 'https://www.fakesite.com/fake-image.jpg'

    def test_create_schema_with_image_missing(self, fake_article, fake_article_missing_elements):
        """ Test that create_schema returns a schema.org, with image missing. """

        article = ArticleSchemaCreator(
            author=fake_article.author,
            title=fake_article.title,
            category=fake_article.category,
            date=fake_article.date,
            logo=fake_article.settings['LOGO'],
            image=fake_article_missing_elements.metadata['image'],
            sitename=fake_article.settings['SITENAME'],
        )

        fake_article_schema = article.create_schema()

        assert 'https://www.fakesite.com/fake-image.jpg' not in fake_article_schema

        assert fake_article_schema['author']['name'] == 'Fake author'
        assert fake_article_schema['publisher']['name'] == 'Fake Site Name'
        assert fake_article_schema['publisher']['logo']['url'] == 'https://www.fakesite.com/fake-logo.jpg'
        assert fake_article_schema['headline'] == 'Fake Title'
        assert fake_article_schema['about'] == 'Fake category'
        assert fake_article_schema['datePublished'] == '2019-04-03 23:49'

    def test_create_schema_with_sitename_missing(self, fake_article, fake_article_missing_elements):
        """ Test that create_schema returns a schema.org, with sitename missing. """

        article = ArticleSchemaCreator(
            author=fake_article.author,
            title=fake_article.title,
            category=fake_article.category,
            date=fake_article.date,
            logo=fake_article.settings['LOGO'],
            image=fake_article.metadata['image'],
            sitename=fake_article_missing_elements.settings['SITENAME'],
        )

        fake_article_schema = article.create_schema()

        assert 'Fake Site Name' not in fake_article_schema
        assert 'logo' not in fake_article_schema

        assert fake_article_schema['author']['name'] == 'Fake author'
        assert fake_article_schema['headline'] == 'Fake Title'
        assert fake_article_schema['about'] == 'Fake category'
        assert fake_article_schema['datePublished'] == '2019-04-03 23:49'
        assert fake_article_schema['image'] == 'https://www.fakesite.com/fake-image.jpg'


class TestBreadcrumbSchemaCreator():
    """ Unit tests for BreadcrumbSchemaCreator. """

    def test_create_schema(self, fake_article):
        """ Test that create_schema returns a valid schema.org (dict) for breadcrumb. """

        breadcrumb = BreadcrumbSchemaCreator(
            output_path='fake_output',
            path='fake_dir/fake_output/fake-file.html',
            sitename=fake_article.settings['SITENAME'],
            siteurl=fake_article.settings['SITEURL'],
        )

        fake_breadcrumb_schema = breadcrumb.create_schema()

        assert fake_breadcrumb_schema['@context'] == "https://schema.org"
        assert fake_breadcrumb_schema['@type'] == "BreadcrumbList"

        assert len(fake_breadcrumb_schema['itemListElement']) == 2

        assert fake_breadcrumb_schema['itemListElement'][0]['@type'] == "ListItem"
        assert fake_breadcrumb_schema['itemListElement'][0]['position'] == 1
        assert fake_breadcrumb_schema['itemListElement'][0]['name'] == "Fake Site Name"
        assert fake_breadcrumb_schema['itemListElement'][0]['item'] == "fakesite.com"

        assert fake_breadcrumb_schema['itemListElement'][1]['@type'] == "ListItem"
        assert fake_breadcrumb_schema['itemListElement'][1]['position'] == 2
        assert fake_breadcrumb_schema['itemListElement'][1]['name'] == "Fake file"
        assert fake_breadcrumb_schema['itemListElement'][1]['item'] == "fakesite.com/fake-file.html"

    def test_create_schema_with_x_elements_in_path(self, fake_article):
        """ Test that create_schema returns a valid schema.org (dict) for a path with x elements. """

        breadcrumb = BreadcrumbSchemaCreator(
            output_path='fake_output',
            path='fake_dir/fake_output/test/blabla/other/kiwi/fake-file.html',
            sitename=fake_article.settings['SITENAME'],
            siteurl=fake_article.settings['SITEURL'],
        )

        fake_breadcrumb_schema = breadcrumb.create_schema()

        assert len(fake_breadcrumb_schema['itemListElement']) == 6

    def test_create_schema_with_no_sitename_no_siteurl(self, fake_article):
        """ Test that create_schema returns incomplete schema.org. """

        breadcrumb = BreadcrumbSchemaCreator(
            output_path='fake_output',
            path='fake_dir/fake_output/fake-file.html',
            sitename='',
            siteurl='',
        )

        fake_breadcrumb_schema = breadcrumb.create_schema()

        assert not fake_breadcrumb_schema['itemListElement'][0]['position'] == 1

    def test_create_schema_with_no_sitename(self, fake_article):
        """ Test that create_schema with siteurl but no sitename returns incomplete schema.org. """

        breadcrumb = BreadcrumbSchemaCreator(
            output_path='fake_output',
            path='fake_dir/fake_output/fake-file.html',
            sitename='',
            siteurl=fake_article.settings['SITEURL'],
        )

        fake_breadcrumb_schema = breadcrumb.create_schema()

        assert not fake_breadcrumb_schema['itemListElement'][0]['position'] == 1

    def test_create_schema_with_no_siteurl(self, fake_article):
        """ Test that create_schema with sitename but no siteurl returns incomplete schema.org. """

        breadcrumb = BreadcrumbSchemaCreator(
            output_path='fake_output',
            path='fake_dir/fake_output/fake-file.html',
            sitename=fake_article.settings['SITENAME'],
            siteurl='',
        )

        fake_breadcrumb_schema = breadcrumb.create_schema()

        assert not fake_breadcrumb_schema['itemListElement'][0]['position'] == 1
