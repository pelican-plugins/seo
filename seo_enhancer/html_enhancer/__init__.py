""" HTML Enhancer : get instances of HTML enhancements. """

from .canonical_url_creator import CanonicalURLCreator
from .article_schema_creator import ArticleSchemaCreator
from .breadcrumb_schema_creator import BreadcrumbSchemaCreator

class HTMLEnhancer():
    """ HTML Enhancer : get instances of HTML enhancements. """

    def __init__(self, article, output_path, path):
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

        self.article_schema = ArticleSchemaCreator(
            author=_author,
            title=_title,
            category=_category,
            date=_date,
            logo=_settings.get('LOGO'),
            image=_image,
            sitename=_settings.get('SITENAME'),
        )

        self.breadcrumb_schema = BreadcrumbSchemaCreator(
            output_path=output_path,
            path=path,
            sitename=_settings.get('SITENAME'),
            siteurl=_settings.get('SITEURL')
        )
