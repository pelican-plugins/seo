"""
Breadcrumb Schema.org creator : Improve URLs display in Google
thanks to breadcrumb set up.
https://schema.org/BreadcrumbList : JSON-LD format.
"""

import os


class BreadcrumbSchemaCreator():
    """
    Get all URLs for a path and build the Breadcrumb schema compliant
    to https://schema.org/BreadcrumbList and Google requirements.
    """

    def __init__(self, output_path, path, sitename, siteurl):
        self._output_path = output_path
        self._path = path
        self._sitename = sitename
        self._siteurl = siteurl

    def _create_paths(self):
        """
        Split the file path, get all elements after the output path.
        By default, output path is 'output/' but it can be changes in Pelican settings.
        Build all paths, for example :
        Path = 'test-dir/output/category/file.html'
        Split path = ['output', 'category', 'file.html']
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

        split_path = self._path.split('/')

        if self._output_path in split_path:
            max_index = split_path.index(self._output_path) + 1

        # Delete all elements before output path, including it
        del split_path[0:max_index]

        breadcrumb_paths = []
        position = 2

        for item in range(1, len(split_path) + 1):

            name = split_path[item-1]
            name = name.replace('-', ' ').capitalize()
            if name.endswith('.html'):
                name = name[:-5]

            full_path = '/'.join(split_path[:item])
            url = os.path.join(self._siteurl, full_path)

            breadcrumb_paths.append({
                'name': name,
                'url': url,
                'position': position
            })

            position += 1

        return breadcrumb_paths

    def create_schema(self):
        """
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
            breadcrumb_schema['itemListElement'].append(
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": self._sitename,
                    "item": self._siteurl
                }
            )

        for item in breadcrumb_items:
            breadcrumb_schema['itemListElement'].append(
                {
                    "@type": "ListItem",
                    "position": item['position'],
                    "name": item['name'],
                    "item": item['url']
                }
            )

        return breadcrumb_schema
