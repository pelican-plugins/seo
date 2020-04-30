""" Units tests for Article Schema Creator. """

from seo.seo_enhancer.html_enhancer import ArticleSchemaCreator


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
        assert fake_article_schema['publisher']['logo']['url'] == \
            'https://www.fakesite.com/fake-logo.jpg'

        assert fake_article_schema['headline'] == 'Fake Title'

        assert fake_article_schema['about'] == 'Fake category'

        assert fake_article_schema['datePublished'] == '2019-04-03 23:49'

        assert fake_article_schema['image'] == 'https://www.fakesite.com/fake-image.jpg'

    def test_create_schema_with_incomplete_article(self, fake_article_missing_elements):
        """
        Test that create_schema returns a schema.org,
        even if article is incomplete.
        """

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

    def test_create_schema_with_author_missing(self, fake_article,
                                               fake_article_missing_elements):
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
        assert fake_article_schema['publisher']['logo']['url'] == \
            'https://www.fakesite.com/fake-logo.jpg'
        assert fake_article_schema['headline'] == 'Fake Title'
        assert fake_article_schema['about'] == 'Fake category'
        assert fake_article_schema['datePublished'] == '2019-04-03 23:49'
        assert fake_article_schema['image'] == 'https://www.fakesite.com/fake-image.jpg'

    def test_create_schema_with_title_missing(self, fake_article,
                                              fake_article_missing_elements):
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
        assert fake_article_schema['publisher']['logo']['url'] == \
            'https://www.fakesite.com/fake-logo.jpg'
        assert fake_article_schema['about'] == 'Fake category'
        assert fake_article_schema['datePublished'] == '2019-04-03 23:49'
        assert fake_article_schema['image'] == 'https://www.fakesite.com/fake-image.jpg'

    def test_create_schema_with_category_missing(self, fake_article,
                                                 fake_article_missing_elements):
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
        assert fake_article_schema['publisher']['logo']['url'] == \
            'https://www.fakesite.com/fake-logo.jpg'
        assert fake_article_schema['headline'] == 'Fake Title'
        assert fake_article_schema['datePublished'] == '2019-04-03 23:49'
        assert fake_article_schema['image'] == 'https://www.fakesite.com/fake-image.jpg'

    def test_create_schema_with_date_missing(self, fake_article,
                                             fake_article_missing_elements):
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
        assert fake_article_schema['publisher']['logo']['url'] == \
            'https://www.fakesite.com/fake-logo.jpg'
        assert fake_article_schema['headline'] == 'Fake Title'
        assert fake_article_schema['about'] == 'Fake category'
        assert fake_article_schema['image'] == 'https://www.fakesite.com/fake-image.jpg'

    def test_create_schema_with_logo_missing(self, fake_article,
                                             fake_article_missing_elements):
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

    def test_create_schema_with_image_missing(self, fake_article,
                                              fake_article_missing_elements):
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
        assert fake_article_schema['publisher']['logo']['url'] == \
            'https://www.fakesite.com/fake-logo.jpg'
        assert fake_article_schema['headline'] == 'Fake Title'
        assert fake_article_schema['about'] == 'Fake category'
        assert fake_article_schema['datePublished'] == '2019-04-03 23:49'

    def test_create_schema_with_sitename_missing(self, fake_article,
                                                 fake_article_missing_elements):
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
