""" HTML Enhancer : get instances of HTML enhancements. """

from .canonical_url_creator import CanonicalURLCreator
from .article_schema_creator import ArticleSchemaCreator
from .breadcrumb_schema_creator import BreadcrumbSchemaCreator


class HTMLEnhancer():
    """ HTML Enhancer : get instances of HTML enhancements. """

    def __init__(self, file, output_path, path):
        _settings = getattr(file, 'settings', None)
        _fileurl = getattr(file, 'url', None)
        _author = getattr(file, 'author', None)
        _date = getattr(file, 'date', None)
        _title = getattr(file, 'title', None)
        _category = getattr(file, 'category', None)
        _image = getattr(file, 'image', None)

        self.article_schema = ArticleSchemaCreator(
            author=_author,
            title=_title,
            category=_category,
            date=_date,
            logo=_settings.get('LOGO'),
            image=_image,
            sitename=_settings.get('SITENAME'),
        )

        self.canonical_link = CanonicalURLCreator(
            siteurl=_settings.get('SITEURL'),
            fileurl=_fileurl,
        )

        self.breadcrumb_schema = BreadcrumbSchemaCreator(
            output_path=output_path,
            path=path,
            sitename=_settings.get('SITENAME'),
            siteurl=_settings.get('SITEURL'),
        )
