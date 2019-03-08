"""
Pelican SEO : a Pelican plugin to improve SEO in static files generator.
Two actions (customizables in plugin settings) : SEO Report and SEO Enhancer.
"""

from pelican import signals

from .settings import SEO_REPORT, SEO_ENHANCER
from .seo_report import SEOReport


# Why need generator ? If not, it's not working
def seo_report_master(generator, metadata):
    print(metadata)
    #print(generator)
    #attrs = vars(generator)
    #print(', '.join("%s: %s" % item for item in attrs.items()))
    seo_report = SEOReport(metadata)
    seo_report.page_title_report()
    seo_report.page_description_report()

def register():
    if SEO_REPORT:
        signals.article_generator_context.connect(seo_report_master)
