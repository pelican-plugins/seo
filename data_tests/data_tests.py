""" Mocks Pelican objects required for the units tests. """

import pytest

from pelican_seo.seo_report import SEOReport


class FakeArticle():
    """ Mock Pelican Article object. """

    def __init__(self, settings, title, description, url, date, content):
        self.settings = settings
        self.title = title
        self.description = description
        self.url = url
        self.date = date
        self.content = content


class FakeDate():
    """ Mock Pelican SafeDate object. """

    def __init__(self, year, month, day, hour, minute):
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        self.hour = int(hour)
        self.minute = int(minute)


@pytest.fixture()
def fake_article():
    """ Create a fake article. """

    fake_date = FakeDate('2019', '04', '03', '23', '49')

    settings = {
        'SITEURL': 'fakesite.com',
    }
    title = 'Fake Title'
    description = 'Fake description'
    url = 'fake-title.html'
    date = fake_date
    content = """<html>
                    <head>
                        <title>Fake Title</title>
                        <meta name='description' content='Fake description' />
                    </head>
                    <body>
                        <h1>Fake content title</h1>
                        <p>Fake content</p>
                        <a href='https://www.fakesite.com'>Fake internal link</a>
                    </body>
                </html>"""

    return FakeArticle(settings, title, description, url, date, content)

@pytest.fixture()
def fake_article_missing_elements():
    """ Create a fake article. """

    fake_date = FakeDate('2019', '04', '03', '23', '49')

    settings = {
        'SITEURL': 'fakesite.com',
    }
    title = ''
    description = ''
    url = 'fake-title.html'
    date = fake_date
    content = """<html>
                    <head>
                    </head>
                    <body>
                        <p>Fake content</p>
                    </body>
                </html>"""

    return FakeArticle(settings, title, description, url, date, content)

@pytest.fixture()
def fake_article_multiple_elements():
    """ Create a fake article with multiple elements. """

    fake_date = FakeDate('2019', '04', '03', '23', '49')

    settings = {
        'SITEURL': 'fakesite.com',
    }
    title = 'Fake Title'
    description = 'Fake description'
    url = 'fake-title.html'
    date = fake_date
    content = """<html>
                    <head>
                        <title>Fake Title</title>
                        <meta name='description' content='Fake description' />
                    </head>
                    <body>
                        <h1>Content title</h1>
                        <p>Fake content</p>
                        <h1>Multiple content title</h1>
                        <a href='https://www.fakesite.com'>Fake internal link</a>
                        <a href='https://www.test.com'>Fake external link</a>
                        <a href='www.fakesite.com/test/'>Fake internal link with path</a>
                    </body>
                </html>"""

    return FakeArticle(settings, title, description, url, date, content)

@pytest.fixture()
def fake_seo_report():
    """ Create a fake seo report instance. """

    return SEOReport()

@pytest.fixture()
def fake_articles_analysis(fake_seo_report, fake_article, fake_article_multiple_elements, fake_article_missing_elements):
    """ Create a fake articles analysis. """

    articles_analysis = []

    articles_analysis.append(fake_seo_report.launch_analysis(fake_article))
    articles_analysis.append(fake_seo_report.launch_analysis(fake_article_missing_elements))
    articles_analysis.append(fake_seo_report.launch_analysis(fake_article_multiple_elements))

    return articles_analysis
