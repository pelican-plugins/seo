""" Improve SEO technical for each article : HTML code and robots.txt file. """

import json

from bs4 import BeautifulSoup

from .html_enhancer import HTMLEnhancer
from .robots_file_creator import RobotsFileCreator

class SEOEnhancer():
    """ Improve SEO technical for each article : HTML code and robots.txt file. """

    def launch_html_enhancer(self, article):
        """
        Call HTMLEnhancer for each article.
        Return a dict with all HTML enhancements.
        """

        html_enhancer = HTMLEnhancer(article)

        html_enhancements = {
            'canonical_tag': html_enhancer.canonical_link.create_url(),
            'article_schema': html_enhancer.schema_article.create_schema(),
        }

        return html_enhancements

    def populate_robots(self, article):
        """ Get all robots rules in article.metadata. Return a dict with rules per url. """

        robots_file = RobotsFileCreator(article.metadata)

        return {
            'article_url': article.url,
            'noindex': robots_file.get_noindex,
            'disallow': robots_file.get_disallow,
        }

    def generate_robots(self, rules):
        """ Create robots.txt file, with noindex and disallow rules for each article URL. """

        with open('output/robots.txt', 'w') as robots_file:
            robots_file.write('User-agent: *')
            for rule in rules:
                if rule.get('noindex'):
                    robots_file.write('\n' + 'Noindex: ' + rule.get('article_url'))
                if rule.get('disallow'):
                    robots_file.write('\n' + 'Disallow: ' + rule.get('article_url'))

    def add_html_to_file(self, enhancements, path):
        """ Open HTML file, add HTML enhancements with bs4 and create the new HTML files. """

        with open(path) as html_file:
            html_content = html_file.read()
            soup = BeautifulSoup(html_content, features="html.parser")

        canonical_tag = soup.new_tag(
            "link",
            rel="canonical",
            href=enhancements.get('canonical_tag')
        )
        soup.head.append(canonical_tag)

        schema_script = soup.new_tag("script", type="application/ld+json")
        soup.head.append(schema_script)

        schema_script = soup.find('script')
        # Json dumps permit to keep dict double quotes instead of simples
        # Google valids schema only with double quotes
        schema_script.append(json.dumps(enhancements.get('article_schema')))

        with open(path, 'w') as html_file:
            html_file.write(soup.prettify())
        