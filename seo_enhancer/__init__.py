""" Improve SEO technical for each article : HTML code and robots.txt file. """

from .robots_file_creator import RobotsFileCreator

class SEOEnhancer():
    """ Improve SEO technical for each article : HTML code and robots.txt file. """

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
