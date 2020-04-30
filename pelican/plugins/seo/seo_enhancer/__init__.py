""" Improve SEO technical for each article and page : HTML code and robots.txt file. """

import json
import logging
import os

from bs4 import BeautifulSoup

from .html_enhancer import HTMLEnhancer
from .robots_file_creator import RobotsFileCreator


logger = logging.getLogger(__name__)


class SEOEnhancer():
    """
    Improve SEO technical for each article and page : HTML code and robots.txt file.
    """

    def launch_html_enhancer(self, file, output_path, path):
        """
        Call HTMLEnhancer for each article and page.
        Return a dict with all HTML enhancements.
        """

        html_enhancer = HTMLEnhancer(file, output_path, path)

        html_enhancements = {
            'canonical_tag': html_enhancer.canonical_link.create_url(),
            'breadcrumb_schema': html_enhancer.breadcrumb_schema.create_schema(),
        }

        if 'pages' not in file.url:
            article_schema = html_enhancer.article_schema.create_schema()
            html_enhancements['article_schema'] = article_schema

        return html_enhancements

    def populate_robots(self, document):
        """
        Get all robots rules in document.metadata.
        Return a dict with rules per url.
        """

        robots_file = RobotsFileCreator(document.metadata)

        return {
            'document_url': document.url,
            'noindex': robots_file.get_noindex,
            'disallow': robots_file.get_disallow,
        }

    def generate_robots(self, rules, output_path):
        """
        Create robots.txt file, with noindex and disallow rules for each document URL.
        """
        if not os.path.isdir(output_path):
            os.mkdir(output_path)

        robots_path = os.path.join(output_path, 'robots.txt')

        with open(robots_path, 'w+') as robots_file:
            robots_file.write('User-agent: *')
            for rule in rules:
                if rule.get('noindex'):
                    robots_file.write('\n' + 'Noindex: ' + rule.get('document_url'))
                if rule.get('disallow'):
                    robots_file.write('\n' + 'Disallow: ' + rule.get('document_url'))

        logger.info("SEO plugin - SEO Enhancement: robots.txt file created")

    def add_html_to_file(self, enhancements, path):
        """
        Open HTML file, add HTML enhancements with bs4 and create the new HTML files.
        """

        with open(path) as html_file:
            html_content = html_file.read()
            soup = BeautifulSoup(html_content, features="html.parser")

        canonical_tag = soup.new_tag(
            "link",
            rel="canonical",
            href=enhancements.get('canonical_tag')
        )
        soup.head.append(canonical_tag)

        position = 0
        for enhancement in enhancements:

            if enhancement.endswith('_schema'):
                schema = enhancement

                schema_script = soup.new_tag("script", type="application/ld+json")
                soup.head.append(schema_script)

                schema_script = soup.findAll('script')[position]
                # Json dumps permit to keep dict double quotes instead of simples
                # Google valids schema only with double quotes
                schema_script.append(
                    json.dumps(enhancements[schema], ensure_ascii=False)
                )

                position += 1

        with open(path, 'w') as html_file:
            html_file.write(soup.prettify())

        logger.info(f"SEO plugin - SEO Enhancement: Done for {path}")
