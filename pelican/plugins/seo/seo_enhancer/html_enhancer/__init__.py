"""HTML Enhancer : get instances of HTML enhancements."""

from pelican.contents import Article, Page

from .article_schema_creator import ArticleSchemaCreator
from .breadcrumb_schema_creator import BreadcrumbSchemaCreator
from .canonical_url_creator import CanonicalURLCreator
from .open_graph import OpenGraph
from .twitter_cards import TwitterCards


class HTMLEnhancer:
    """HTML Enhancer : get instances of HTML enhancements."""

    def __init__(self, file, output_path, path, open_graph=False, twitter_cards=False):
        _file_type = "website"  # Default value
        if isinstance(file, Article):
            _file_type = "article"
        elif isinstance(file, Page):
            _file_type = "page"

        _settings = file.settings
        _author = getattr(file, "author", None)
        _date = getattr(file, "date", None)
        _title = getattr(file, "title", None)
        _category = getattr(file, "category", None)
        _image = getattr(file, "image", None)
        _metadata = getattr(file, "metadata", None)

        self.article_schema = ArticleSchemaCreator(
            author=_author,
            title=_title,
            category=_category,
            date=_date,
            logo=_settings.get("LOGO"),
            image=_image,
            sitename=_settings.get("SITENAME"),
        )

        # The canonical URL must be built with custom metadata if filled.
        # This can come from either the canonical or save_as field.
        # If both are absent, fallback to the default URL name
        canonical = _metadata.get("external_canonical")
        if canonical:
            self.canonical_link = CanonicalURLCreator(
                siteurl=canonical,
                fileurl=None,
            )
        else:
            save_as = _metadata.get("save_as")
            _fileurl = save_as if save_as else file.url
            self.canonical_link = CanonicalURLCreator(
                siteurl=_settings.get("SITEURL"),
                fileurl=_fileurl,
            )

        self.breadcrumb_schema = BreadcrumbSchemaCreator(
            output_path=output_path,
            path=path,
            sitename=_settings.get("SITENAME"),
            siteurl=_settings.get("SITEURL"),
        )

        if open_graph:
            self.open_graph = OpenGraph(
                siteurl=_settings.get("SITEURL"),
                fileurl=_fileurl,
                file_type=_file_type,
                title=_metadata.get("og_title") or _title,
                description=_metadata.get("og_description")
                or _metadata.get("description"),
                image=_metadata.get("og_image") or _image,
                locale=_settings.get("LOCALE"),
            )

            if twitter_cards:
                self.twitter_cards = TwitterCards(
                    tw_account=_metadata.get("tw_account"),
                )
