""" Article Schema.org creator : Improve articles display in Google if all fields are fill in. """

import datetime

class ArticleSchemaCreator():
    """
    Get all field values and build the Article schema compliant
    to https://schema.org/Article and Google requirements.
    """

    def __init__(self, author, title, category, date, logo, image, sitename):
        self.author = author.name
        self.title = title
        self.category = category.name
        self.publication_date = date
        self.logo = logo
        self.image = image
        self.sitename = sitename

    def _convert_date(self, date):
        """ Get SafeDate Pelican object and return date in string. """

        date_time = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute)
        return date_time.strftime("%Y-%m-%d %H:%M")

    def create_schema(self):
        """
        Create Article schema.
        Schema : {
            "@context": "http://schema.org",
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
            "@context": "http://schema.org",
            "@type": "Article",
        }

        if self.author:
            schema_article["author"] = {
                "@type": "Person",
                "name": self.author
            }

        if self.sitename:
            schema_article["publisher"] = {
                "@type": "Organization",
                "name": self.sitename,
            }

            if self.logo:
                schema_article["publisher"]["logo"] = {
                    "@type": "ImageObject",
                    "url": self.logo
                }

        if self.title:
            schema_article["headline"] = self.title

        if self.category:
            schema_article["about"] = self.category

        if self.publication_date:
            schema_article["datePublished"] = self._convert_date(self.publication_date)

        if self.image:
            schema_article["image"] = self.image

        return schema_article
