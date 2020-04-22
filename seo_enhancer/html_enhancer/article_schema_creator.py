"""
Article Schema.org creator : Improve articles display in Google
if all fields are fill in.
https://schema.org/Article : JSON-LD format.
"""

import datetime


class ArticleSchemaCreator():
    """
    Get all field values and build the Article schema compliant
    to https://schema.org/Article and Google requirements.
    """

    def __init__(self, author, title, category, date, logo, image, sitename):
        self._author = author.name
        self._title = title
        self._category = category.name
        self._publication_date = date
        self._logo = logo
        self._image = image
        self._sitename = sitename

    def _convert_date(self, date):
        """ Get SafeDate Pelican object and return date in string. """

        date_time = datetime.datetime(
            date.year,
            date.month,
            date.day,
            date.hour,
            date.minute
        )
        return date_time.strftime("%Y-%m-%d %H:%M")

    def create_schema(self):
        """
        Create Article schema.
        Schema : {
            "@context": "https://schema.org",
            "@type": "Article",
            "author": {
                "@type": "Person",
                "name": :author:
            },
            "publisher": {
                "@type": "Organization",
                "name": :sitename:,
                "logo": {
                    "@type": "ImageObject",
                    "url": :logo:
                }
            },
            "headline": :title:,
            "about": :category:,
            "datePublished": :publication_date:,
            "image": :image:
        }
        """

        schema_article = {
            "@context": "https://schema.org",
            "@type": "Article",
        }

        if self._author:
            schema_article["author"] = {
                "@type": "Person",
                "name": self._author
            }

        if self._sitename:
            schema_article["publisher"] = {
                "@type": "Organization",
                "name": self._sitename,
            }

            if self._logo:
                schema_article["publisher"]["logo"] = {
                    "@type": "ImageObject",
                    "url": self._logo
                }

        if self._title:
            schema_article["headline"] = self._title

        if self._category:
            schema_article["about"] = self._category

        if self._publication_date:
            schema_article["datePublished"] = self._convert_date(self._publication_date)

        if self._image:
            schema_article["image"] = self._image

        return schema_article
