"""
Pelican SEO : a Pelican plugin to improve SEO in static files generator.
Some actions are customizables in plugin settings.
"""

import os

from pelican import signals
from pelican.generators import ArticlesGenerator, PagesGenerator

from .settings import SEO_REPORT, SEO_ENHANCER, ARTICLES_LIMIT
from .seo_report import SEOReport
from .seo_enhancer import SEOEnhancer


def run_full_plugin(generators):
    """ Run all plugin elements if it's active in settings. """

    for generator in generators:

        if not generator.settings.get('SITEURL'):
            raise Exception('You must fill in SITEURL variable in pelicanconf.py to use SEO plugin.')

        site_name = generator.settings.get('SITENAME')

        if isinstance(generator, ArticlesGenerator):

            seo_report = SEOReport()
            articles_analysis = []

            seo_enhancer = SEOEnhancer()
            robots_rules = []

            # Launch analysis and enhancement for each articles. User can limit this number.
            for _, article in zip(range(ARTICLES_LIMIT), generator.articles):
                analysis = seo_report.launch_analysis(article)
                articles_analysis.append(analysis)

                article_metadata = seo_enhancer.populate_robots(article)
                robots_rules.append(article_metadata)

            seo_report.generate(site_name, articles_analysis)
            seo_enhancer.generate_robots(robots_rules)

        #elif isinstance(generator, PagesGenerator):
        #    for page in generator.pages:
        #        print(page)

def run_seo_report(generators):
    """ Run SEO report plugin only if it's active in settings. """

    for generator in generators:

        if not generator.settings.get('SITEURL'):
            raise Exception('You must fill in SITEURL variable in pelicanconf.py to use SEO plugin.')

        site_name = generator.settings.get('SITENAME')

        if isinstance(generator, ArticlesGenerator):

            seo_report = SEOReport()
            articles_analysis = []

            # Launch analysis for each articles. User can limit this number.
            for _, article in zip(range(ARTICLES_LIMIT), generator.articles):
                analysis = seo_report.launch_analysis(article)
                articles_analysis.append(analysis)

            seo_report.generate(site_name, articles_analysis)

def run_seo_enhancer(generators):
    """ Run SEO enhancement plugin only if it's active in settings. """

    for generator in generators:

        if isinstance(generator, ArticlesGenerator):

            seo_enhancer = SEOEnhancer()
            robots_rules = []

            # Launch enhancement for each articles. User can limit this number.
            for _, article in zip(range(ARTICLES_LIMIT), generator.articles):
                article_metadata = seo_enhancer.populate_robots(article)
                robots_rules.append(article_metadata)

            seo_enhancer.generate_robots(robots_rules)

def run_html_enhancer(path, context):
    """ Run HTML enhancements """

    if not context.get('SITEURL'):
        raise Exception('You must fill in SITEURL variable in pelicanconf.py to use SEO plugin.')

    if context.get('article'):
        seo_enhancer = SEOEnhancer()
        html_enhancements = seo_enhancer.launch_html_enhancer(context['article'])
        seo_enhancer.add_html_to_file(html_enhancements, path)


def register():
    if SEO_REPORT and SEO_ENHANCER:
        signals.all_generators_finalized.connect(run_full_plugin)
        print("------ SEO Plugin -------")
        print("--- SEO Report : Done ---")
        print("--- SEO Enhancement : Done ---")

    elif SEO_REPORT:
        signals.all_generators_finalized.connect(run_seo_report)
        print("------ SEO Plugin -------")
        print("--- SEO Report : Done ---")

    elif SEO_ENHANCER:
        signals.all_generators_finalized.connect(run_seo_enhancer)
        signals.content_written.connect(run_html_enhancer)
        print("------ SEO Plugin -------")
        print("--- SEO Enhancement : Done ---")
