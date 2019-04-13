"""
Pelican SEO : a Pelican plugin to improve SEO in static files generator.
Some actions are customizables in plugin settings.
"""

from pelican import signals
from pelican.generators import ArticlesGenerator, PagesGenerator

from .settings import SEO_REPORT, SEO_ENHANCER, ARTICLES_LIMIT
from .seo_report import SEOReport


def run_plugin(generators):

    for generator in generators:

        if not generator.settings.get('SITEURL'):
            raise Exception('You must fill in SITEURL variable in pelicanconf.py to use SEO plugin.')

        site_name = generator.settings.get('SITENAME')

        if isinstance(generator, ArticlesGenerator):

            seo_report = SEOReport()

            articles_analysis = []

            # Launch analysis for each articles. User can limit this number.
            for _, article in zip(range(ARTICLES_LIMIT), generator.articles):

                #article_date.append = article.date

                analysis = seo_report.launch_analysis(article)
                articles_analysis.append(analysis)

            seo_report.generate(site_name, articles_analysis)

        #elif isinstance(generator, PagesGenerator):
        #    for page in generator.pages:
        #        print(page)


def register():
    if SEO_REPORT:
        signals.all_generators_finalized.connect(run_plugin)
