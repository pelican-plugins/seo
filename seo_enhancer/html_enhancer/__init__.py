""" HTML Enhancer : get instances of HTML enhancements. """

from .canonical_url_creator import CanonicalURLCreator
from .article_schema_creator import ArticleSchemaCreator

class HTMLEnhancer():
    """ HTML Enhancer : get instances of HTML enhancements. """

    def __init__(self, article):
        _settings = getattr(article, 'settings', None)
        _file_url = getattr(article, 'url', None)
        _author = getattr(article, 'author', None)
        _date = getattr(article, 'date', None)
        _title = getattr(article, 'title', None)
        _category = getattr(article, 'category', None)
        _image = getattr(article, 'image', None)

        self.canonical_link = CanonicalURLCreator(
            site_url=_settings.get('SITEURL'),
            file_url=_file_url,
        )

        self.schema_article = ArticleSchemaCreator(
            author=_author,
            title=_title,
            category=_category,
            date=_date,
            logo=_settings.get('LOGO'),
            image=_image,
            sitename=_settings.get('SITENAME'),
        )
