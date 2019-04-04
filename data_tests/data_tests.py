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
                        <a href=''>Fake internal link</a>
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
def fake_seo_report():
    """ Create a fake seo report instance. """

    return SEOReport()
