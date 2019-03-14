"""
Pelican SEO : a Pelican plugin to improve SEO in static files generator.
Two actions (customizables in plugin settings) : SEO Report and SEO Enhancer.
"""

from pelican import signals
from pelican.generators import ArticlesGenerator, PagesGenerator


from .settings import SEO_REPORT, SEO_ENHANCER
from .seo_report import SEOReport


def run_plugin(generators):

    for generator in generators:
        if isinstance(generator, ArticlesGenerator):

            for article in generator.articles:
                seo_report = SEOReport(article)
                seo_report.page_title_report()
                seo_report.page_description_report()
                seo_report.content_title_report()
                print("--------------------")

        #elif isinstance(generator, PagesGenerator):
        #    for page in generator.pages:
        #        print(page)


def register():
    if SEO_REPORT:
        signals.all_generators_finalized.connect(run_plugin)
