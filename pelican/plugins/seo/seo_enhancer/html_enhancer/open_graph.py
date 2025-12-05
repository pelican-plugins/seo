import locale
from urllib import parse

from pelican.utils import strftime


class OpenGraph:
    """
    Get all Open Graph elements according to
    https://developers.facebook.com/docs/sharing/webmasters#markup.
    """

    def __init__(
        self, sitename, siteurl, fileurl, file_type, title, description, image, locale
    ) -> None:
        self.sitename = sitename
        self.siteurl = siteurl
        self.fileurl = fileurl
        self.type = file_type
        self.title = title
        self.description = description
        self.image = image
        self.locale = locale

    def _create_absolute_fileurl(self):
        """Join site URL and file path."""
        if not self.siteurl.endswith("/"):
            self.siteurl += "/"

        if self.fileurl.startswith("/"):
            self.fileurl = self.fileurl[1:]

        file_url = parse.urljoin(self.siteurl, self.fileurl)
        return file_url

    def _get_locale(self) -> str:
        """
        Check first in the locale defined by the user in Pelican settings.
        Fallback with the system default locale.
        Can return None if the getdefaultlocale() failed to find a value.
        """
        og_locale = None
        for setted_locale in self.locale:
            if setted_locale:
                og_locale = setted_locale
                break

        if not og_locale:
            default_locale = locale.getdefaultlocale()
            if default_locale:
                # Get only the language, we don't need the encoding
                og_locale = default_locale[0]

        return og_locale

    def create_tags(self) -> dict:
        """
        Compute all Open Graph elements and return them in a ready-to-use dict.
        :url: and :type: are filled thanks to Pelican and can't be None.
        """
        open_graph_tags = {}

        if self.sitename:
            open_graph_tags["site_name"] = self.sitename

        open_graph_tags["url"] = self._create_absolute_fileurl()
        open_graph_tags["type"] = self.type

        if self.title:
            open_graph_tags["title"] = self.title

        if self.description:
            open_graph_tags["description"] = self.description

        if self.image:
            open_graph_tags["image"] = self.image

        locale = self._get_locale()
        if locale:
            open_graph_tags["locale"] = locale

        return open_graph_tags


class OpenGraphArticle:
    """
    Get all Open Graph elements for an Article according to
    https://ogp.me/?#no_vertical.
    """

    def __init__(self, date, modified, category, tags, author) -> None:
        self.date = date
        self.modified = modified
        self.category = category
        self.tags = tags
        self.author = author

    def create_tags(self) -> dict:
        """
        Compute all Open Graph elements for Article and return them in a ready-to-use
        dict.
        """
        tags = {}
        tags["published_time"] = strftime(self.date, "%Y-%m-%d")
        if self.modified is not None:
            tags["modified_time"] = strftime(self.modified, "%Y-%m-%d")
        if self.category is not None:
            tags["section"] = self.category
        if self.tags is not None and self.tags:
            tags["tags"] = self.tags
        if self.author is not None:
            tags["author"] = self.author
        return tags
