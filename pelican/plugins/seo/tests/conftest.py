"""Mocks Pelican objects required for the units tests."""

import pytest

from seo.seo_enhancer import SEOEnhancer
from seo.seo_report import SEOReport


class FakeArticle:
    """Mock Pelican Article object."""

    def __init__(
        self,
        settings,
        metadata,
        title,
        description,
        url,
        date,
        content,
        author,
        category,
    ):
        self.settings = settings
        self.metadata = metadata
        self.title = title
        self.description = description
        self.url = url
        self.date = date
        self.content = content
        self.author = author
        self.category = category


class FakeDate:
    """Mock Pelican SafeDate object."""

    def __init__(self, year, month, day, hour, minute):
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        self.hour = int(hour)
        self.minute = int(minute)


class FakeAuthor:
    """Mock Pelican Author object."""

    def __init__(self, name):
        self.name = name


class FakeCategory:
    """Mock Pelican Category object."""

    def __init__(self, name):
        self.name = name


@pytest.fixture()
def fake_article():
    """Create a fake article."""

    settings = {
        "SITEURL": "https://www.fakesite.com",
        "SITENAME": "Fake Site Name",
        "LOGO": "https://www.fakesite.com/fake-logo.jpg",
        "LOCALE": ["fr_FR"],
    }
    metadata = {
        "noindex": True,
        "disallow": True,
        "image": "https://www.fakesite.com/fake-image.jpg",
        "og_title": "OG Title",
        "og_description": "OG Description",
        "og_image": "https://www.fakesite.com/og-image.jpg",
        "tw_account": "@TestTWCards",
    }
    title = "Fake Title"
    description = "Fake description"
    url = "fake-title.html"
    date = FakeDate("2019", "04", "03", "23", "49")
    author = FakeAuthor(name="Fake author")
    category = FakeCategory(name="Fake category")
    content = """<html>
                    <head>
                        <title>Fake Title</title>
                        <meta name='description' content='Fake description' />
                    </head>
                    <body>
                        <h1>Fake content title</h1>
                        <p>Fake content 🙃</p>
                        <a href='https://www.fakesite.com'>Fake internal link</a>
                        <p>Fake content with <code>inline code</code></p>
                        <p>Fake content with "<a href="https://www.fakesite.com">Fake inline internal link</a>"</p>
                    </body>
                </html>"""

    return FakeArticle(
        settings=settings,
        metadata=metadata,
        title=title,
        description=description,
        url=url,
        date=date,
        content=content,
        author=author,
        category=category,
    )


@pytest.fixture()
def fake_article_missing_elements():
    """Create a fake article with missing elements."""

    settings = {
        "SITEURL": "https://www.fakesite.com",
        "SITENAME": "",
        "LOGO": "",
    }
    metadata = {
        "noindex": True,
        "image": "",
        "tw_account": None,
    }
    title = ""
    description = ""
    url = "fake-title.html"
    date = FakeDate("2019", "04", "03", "23", "49")
    author = FakeAuthor(name="")
    category = FakeCategory(name="")
    content = """<html>
                    <head>
                    </head>
                    <body>
                        <p>Fake content 🙃</p>
                    </body>
                </html>"""

    return FakeArticle(
        settings=settings,
        metadata=metadata,
        title=title,
        description=description,
        url=url,
        date=date,
        content=content,
        author=author,
        category=category,
    )


@pytest.fixture()
def fake_article_multiple_elements():
    """Create a fake article with multiple elements."""

    settings = {
        "SITEURL": "https://www.fakesite.com",
        "SITENAME": "Fake Site Name",
        "LOGO": "https://www.fakesite.com/fake-logo.jpg",
    }
    metadata = {}
    # 70 character long title, needed for SEO report
    title = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam morbi."
    # 150 character long description, needed for SEO report
    description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec sit amet lectus ante. Phasellus nec augue neque. Curabitur aliquet sem sed quam libero."
    url = "fake-title.html"
    date = FakeDate("2019", "04", "03", "23", "49")
    author = FakeAuthor(name="Fake author")
    category = FakeCategory(name="Fake category")
    content = """<html>
                    <head>
                        <title>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam morbi.</title>
                        <meta name='description' content='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec sit amet lectus ante. Phasellus nec augue neque. Curabitur aliquet sem sed quam libero.' />
                    </head>
                    <body>
                        <h1>Content title</h1>
                        <p>Fake content 🙃</p>
                        <h1>Multiple content title</h1>
                        <a href='https://www.fakesite.com'>Fake internal link</a>
                        <a href='https://www.test.com'>Fake external link</a>
                        <a href='https://www.fakesite.com/test/'>Fake internal path link</a>
                        <a>a tag without href attribute</a>
                    </body>
                </html>"""

    return FakeArticle(
        settings=settings,
        metadata=metadata,
        title=title,
        description=description,
        url=url,
        date=date,
        content=content,
        author=author,
        category=category,
    )


@pytest.fixture()
def fake_seo_report():
    """Create a fake seo report instance."""

    return SEOReport()


@pytest.fixture()
def fake_robots_rules(
    fake_seo_enhancer,
    fake_article,
    fake_article_multiple_elements,
    fake_article_missing_elements,
):
    """Create a fake robots rules."""

    robots_rules = []

    robots_rules.append(fake_seo_enhancer.populate_robots(fake_article))
    robots_rules.append(
        fake_seo_enhancer.populate_robots(fake_article_missing_elements)
    )
    robots_rules.append(
        fake_seo_enhancer.populate_robots(fake_article_multiple_elements)
    )

    return robots_rules


@pytest.fixture()
def fake_articles_analysis(
    fake_seo_report,
    fake_article,
    fake_article_multiple_elements,
    fake_article_missing_elements,
):
    """Create a fake articles analysis."""

    articles_analysis = []

    articles_analysis.append(fake_seo_report.launch_analysis(fake_article))
    articles_analysis.append(
        fake_seo_report.launch_analysis(fake_article_missing_elements)
    )
    articles_analysis.append(
        fake_seo_report.launch_analysis(fake_article_multiple_elements)
    )

    return articles_analysis


@pytest.fixture()
def fake_seo_enhancer():
    """Create a fake seo enhancer instance."""

    return SEOEnhancer()
