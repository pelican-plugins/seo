"""
Ave SEO! is a Pelican plugin to helps you improve your Pelican site SEO to reach
the tops positions on search engines like Qwant, DuckDuckGo or Google.
===================================================================================

It generates a SEO report and SEO enhancements.
You can enable / disable the main features in the plugin settings.
For the SEO report, you can limit the number of analysis in the plugin settings too.

Author : Maëva Brunelles <https://github.com/MaevaBrunelles>
License : GNU AFFERO GENERAL PUBLIC LICENSE Version 3
"""

from pelican import signals
from pelican.generators import ArticlesGenerator, PagesGenerator

from .settings import SEO_REPORT, SEO_ENHANCER, ARTICLES_LIMIT, PAGES_LIMIT
from .seo_report import SEOReport
from .seo_enhancer import SEOEnhancer


def run_seo_report_robots_file(generators):
    """ Run all plugin elements if it's active in settings. """

    seo_report = SEOReport()
    files_analysis = []

    seo_enhancer = SEOEnhancer()
    robots_rules = []

    for generator in generators:

        if not generator.settings.get('SITEURL'):
            raise Exception('You must fill in SITEURL variable in pelicanconf.py to use Ave SEO! plugin.')

        site_name = generator.settings.get('SITENAME')
        output_path = generator.output_path

        if isinstance(generator, ArticlesGenerator):
            for index, article in enumerate(generator.articles, 1):
                # Launch robots file creation for each article.
                article_metadata = seo_enhancer.populate_robots(article=article)
                robots_rules.append(article_metadata)
                # Launch analysis for a limited article number. User can set the limit.
                if index <= ARTICLES_LIMIT:
                    analysis = seo_report.launch_analysis(article=article)
                    files_analysis.append(analysis)

        if isinstance(generator, PagesGenerator):
            for index, page in enumerate(generator.pages, 1):
                page_metadata = seo_enhancer.populate_robots(article=page)
                robots_rules.append(page_metadata)

                if index <= PAGES_LIMIT:
                    analysis = seo_report.launch_analysis(article=page)
                    files_analysis.append(analysis)

    seo_report.generate(
        site_name=site_name,
        articles_analysis=files_analysis
    )
    seo_enhancer.generate_robots(
        rules=robots_rules,
        output_path=output_path,
    )

def run_seo_report(generators):
    """ Run SEO report plugin only if it's active in settings. """

    seo_report = SEOReport()
    files_analysis = []

    for generator in generators:

        if not generator.settings.get('SITEURL'):
            raise Exception('You must fill in SITEURL variable in pelicanconf.py to use Ave SEO! plugin.')

        site_name = generator.settings.get('SITENAME')

        if isinstance(generator, ArticlesGenerator):
            # Launch analysis for each article. User can limit this number.
            for _, article in zip(range(ARTICLES_LIMIT), generator.articles):
                analysis = seo_report.launch_analysis(article=article)
                files_analysis.append(analysis)

        if isinstance(generator, PagesGenerator):
            # Launch analysis each page. User can limit this number.
            for _, page in zip(range(PAGES_LIMIT), generator.pages):
                analysis = seo_report.launch_analysis(article=page)
                files_analysis.append(analysis)

    seo_report.generate(
        site_name=site_name,
        articles_analysis=files_analysis
    )

def run_robots_file(generators):
    """ Run SEO enhancement plugin only if it's active in settings. """

    seo_enhancer = SEOEnhancer()
    robots_rules = []

    for generator in generators:

        output_path = generator.output_path

        if isinstance(generator, ArticlesGenerator):
            for article in generator.articles:
                article_metadata = seo_enhancer.populate_robots(article=article)
                robots_rules.append(article_metadata)

        if isinstance(generator, PagesGenerator):
            for page in generator.pages:
                page_metadata = seo_enhancer.populate_robots(article=page)
                robots_rules.append(page_metadata)

    seo_enhancer.generate_robots(
        rules=robots_rules,
        output_path=output_path,
    )

def run_html_enhancer(path, context):
    """ Run HTML enhancements """

    if not context.get('SITEURL'):
        raise Exception('You must fill in SITEURL variable in pelicanconf.py to use Ave SEO! plugin.')

    if context.get('article'):
        seo_enhancer = SEOEnhancer()
        html_enhancements = seo_enhancer.launch_html_enhancer(
            file=context['article'],
            output_path=context.get('OUTPUT_PATH'),
            path=path,
        )
        seo_enhancer.add_html_to_file(
            enhancements=html_enhancements,
            path=path,
        )

    elif context.get('page'):
        seo_enhancer = SEOEnhancer()
        html_enhancements = seo_enhancer.launch_html_enhancer(
            file=context['page'],
            output_path=context.get('OUTPUT_PATH'),
            path=path,
        )
        seo_enhancer.add_html_to_file(
            enhancements=html_enhancements,
            path=path,
        )


def register():
    print("Ave SEO! plugin initialized")

    if SEO_REPORT and SEO_ENHANCER:
        signals.all_generators_finalized.connect(run_seo_report_robots_file)
        signals.content_written.connect(run_html_enhancer)

    elif SEO_REPORT:
        signals.all_generators_finalized.connect(run_seo_report)

    elif SEO_ENHANCER:
        signals.all_generators_finalized.connect(run_robots_file)
        signals.content_written.connect(run_html_enhancer)
