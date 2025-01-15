"""
Breadcrumb Schema.org creator : Improve URLs display in Google
thanks to breadcrumb set up.
https://schema.org/BreadcrumbList : JSON-LD format.
"""

import os
from pathlib import Path


class BreadcrumbSchemaCreator:
    """
    Get all URLs for a path and build the Breadcrumb schema compliant
    to https://schema.org/BreadcrumbList and Google requirements.
    """

    def __init__(self, output_path, path, sitename, siteurl):
        self._output_path = output_path
        self._path = path
        self._sitename = sitename
        self._siteurl = siteurl

    def _extract_file_path_from_path(self) -> tuple:
        """
        Normalize paths thanks to pathlib,
        and get the file path by discarding output path.
        By default, output path is 'output/' but it can be changed in Pelican settings.
        """
        path = Path(self._path).resolve()
        output_path = Path(self._output_path).resolve()

        file_path = path.relative_to(output_path)

        return file_path.parts

    def _create_paths(self):
        """Build all paths for the breadcrumb.

        Example with a file_path == ("category", "file.html")
        Position begins at 2, as number 1 is dedicated to the index page.
        Returns list of dicts :
        [
            {
                'position': 2,
                'name': 'Category',
                'url': ':siteurl:/category'
            },
            {
                'position': 3,
                'name': 'File',
                'url': ':siteurl:/category/file.html'
            },
        ]
        """
        file_path = self._extract_file_path_from_path()

        breadcrumb_paths = []
        position = 2

        for item in range(1, len(file_path) + 1):
            name = file_path[item - 1]
            name = name.replace("-", " ").capitalize()
            if name.endswith(".html"):
                name = name[:-5]

            full_path = "/".join(file_path[:item])
            url = os.path.join(self._siteurl, full_path)

            breadcrumb_paths.append({"name": name, "url": url, "position": position})

            position += 1

        return breadcrumb_paths

    def create_schema(self):
        """Create the schema.

        Schema = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": :n=1:,
                    "name": :Sitename:,
                    "item": :SITEURL:
                },
                {
                    "@type": "ListItem",
                    "position": :n+1:,
                    "name": :name:,
                    "item": :url:
                },
                {
                    "@type": "ListItem",
                    "position": :n+x:,
                    "name": :name:,
                    "item": :url:
                }
            ]
        }
        """

        breadcrumb_items = self._create_paths()

        breadcrumb_schema = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [],
        }

        if self._sitename and self._siteurl:
            breadcrumb_schema["itemListElement"].append(
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": self._sitename,
                    "item": self._siteurl,
                }
            )

        for item in breadcrumb_items:
            breadcrumb_schema["itemListElement"].append(
                {
                    "@type": "ListItem",
                    "position": item["position"],
                    "name": item["name"],
                    "item": item["url"],
                }
            )

        return breadcrumb_schema
