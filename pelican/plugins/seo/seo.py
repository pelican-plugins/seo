"""
SEO is a Pelican plugin to helps you improve your Pelican site SEO to
reach the tops positions on search engines like Qwant, DuckDuckGo or Google.
===================================================================================

It generates a SEO report and SEO enhancements.
You can enable / disable the main features in the plugin settings.
For the SEO report, you can limit the number of analysis
in the plugin settings too.

Author : Maëva Brunelles <https://github.com/MaevaBrunelles>
License : GNU AFFERO GENERAL PUBLIC LICENSE Version 3
"""

import logging

from pelican import signals
from pelican.generators import ArticlesGenerator, PagesGenerator

from . import settings as default_plugin_settings
from .seo_enhancer import SEOEnhancer
from .seo_report import SEOReport

logger = logging.getLogger(__name__)


def plugin_initializer(settings):
    """Raise if SITEURL parameter is not set in Pelican settings."""

    if not settings.settings.get("SITEURL"):
        raise Exception(
            "You must fill in SITEURL variable in pelicanconf.py \
            to use SEO plugin."
        )

    logger.info("SEO plugin initialized")


def get_plugin_settings(context):
    """Get settings in the Pelican configuration file from the given context.

    .. note:: Pelican's settings take precedence over the plugin's default settings.

    SEO report settings:

        - SEO_REPORT
        - SEO_ARTICLES_LIMIT
        - SEO_PAGES_LIMIT

    SEO enhancer settings:

        - SEO_ENHANCER
        - SEO_ENHANCER_OPEN_GRAPH
        - SEO_ENHANCER_TWITTER_CARDS

    :return: Dictionary of settings for the plugin
    :rtype: <dict>
    """

    def _get_seo_variables(settings):
        """Get variables starting with 'SEO_' & values in the given dictionary.

        :rtype: <dict>
        """
        return {
            name: value for name, value in settings.items() if name.startswith("SEO_")
        }

    plugin_settings = _get_seo_variables(settings=vars(default_plugin_settings))
    plugin_settings.update(_get_seo_variables(settings=context))

    return plugin_settings


def run_seo_report(generators):
    """Run SEO report creation if SEO_REPORT is enabled in settings."""

    plugin_settings = get_plugin_settings(generators[0].context)
    if not plugin_settings["SEO_REPORT"]:
        return

    seo_report = SEOReport()
    documents_analysis = []
    site_name = generators[0].context.get("SITENAME")

    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            # Launch analysis for each article. User can limit this number.
            for _, article in zip(
                range(plugin_settings["SEO_ARTICLES_LIMIT"]), generator.articles
            ):
                analysis = seo_report.launch_analysis(document=article)
                documents_analysis.append(analysis)

        if isinstance(generator, PagesGenerator):
            # Launch analysis each page. User can limit this number.
            for _, page in zip(
                range(plugin_settings["SEO_PAGES_LIMIT"]), generator.pages
            ):
                analysis = seo_report.launch_analysis(document=page)
                documents_analysis.append(analysis)

    seo_report.generate(site_name=site_name, documents_analysis=documents_analysis)


def run_robots_file(generators):
    """
    Run robots.txt file creation if SEO_ENHANCER
    is enabled in settings.
    """
    plugin_settings = get_plugin_settings(generators[0].context)
    if not plugin_settings["SEO_ENHANCER"]:
        return

    seo_enhancer = SEOEnhancer()
    robots_rules = []
    output_path = generators[0].output_path

    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            for article in generator.articles:
                article_metadata = seo_enhancer.populate_robots(document=article)
                robots_rules.append(article_metadata)

        if isinstance(generator, PagesGenerator):
            for page in generator.pages:
                page_metadata = seo_enhancer.populate_robots(document=page)
                robots_rules.append(page_metadata)

    seo_enhancer.generate_robots(
        rules=robots_rules,
        output_path=output_path,
    )


def run_html_enhancer(path, context):
    """Run HTML enhancements if SEO_ENHANCER is enabled in settings."""
    plugin_settings = get_plugin_settings(context)

    seo_enhancer_setting = plugin_settings["SEO_ENHANCER"]
    if not seo_enhancer_setting:
        return

    open_graph_setting = plugin_settings["SEO_ENHANCER_OPEN_GRAPH"]
    twitter_cards_setting = plugin_settings["SEO_ENHANCER_TWITTER_CARDS"]

    if (open_graph_setting or twitter_cards_setting) and not seo_enhancer_setting:
        raise Exception(
            "You must enable SEO_ENHANCER setting to use social medias features."
        )

    if twitter_cards_setting and not open_graph_setting:
        raise Exception("You must enable Open Graph feature to use Twitter Cards.")

    content_file = None
    if context.get("article"):
        content_file = context["article"]
    elif context.get("page"):
        content_file = context["page"]

    if content_file:
        seo_enhancer = SEOEnhancer()
        html_enhancements = seo_enhancer.launch_html_enhancer(
            file=content_file,
            output_path=context.get("OUTPUT_PATH"),
            path=path,
            open_graph=open_graph_setting,
            twitter_cards=twitter_cards_setting,
        )
        seo_enhancer.add_html_to_file(
            enhancements=html_enhancements,
            path=path,
        )


def register():
    """Register the plugin."""

    signals.initialized.connect(plugin_initializer)

    # Seo report
    signals.all_generators_finalized.connect(run_seo_report)

    # Seo enhancer
    signals.all_generators_finalized.connect(run_robots_file)
    signals.content_written.connect(run_html_enhancer)
