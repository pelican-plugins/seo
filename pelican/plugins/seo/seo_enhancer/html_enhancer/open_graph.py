import locale
from urllib import parse


class OpenGraph:
    """
    Get all Open Graph elements according to
    https://developers.facebook.com/docs/sharing/webmasters#markup.
    """

    def __init__(
        self, siteurl, fileurl, file_type, title, description, image, locale
    ) -> None:
        self.siteurl = siteurl
        self.fileurl = fileurl
        self.type = file_type
        self.title = title
        self.description = description
        self.image = image
        self.locale = locale

    def _create_absolute_fileurl(self):
        """Join site URL and file path."""

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
