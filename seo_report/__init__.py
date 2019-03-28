"""
Generate a SEO report by calling SEO analyzers for each content.
"""

import os

from jinja2 import Environment, FileSystemLoader

from .seo_analyzer import SEOAnalyzer


class SEOReport():
    """ Generate a SEO report by calling SEO analyzers for each content. """

    PAGE_TITLE_RECOMMENDED_LENGTH = range(60, 71)
    PAGE_DESCRIPTION_RECOMMENDED_LENGTH = range(150, 161)

    def launch_analysis(self, article):
        """
        Launch SEO analysis for an article.
        Return a dict with article and his analysis.
        """

        seo_analysis = SEOAnalyzer(article)
        article_analysis = {
            "article": article.url,
            "seo_analysis": {
                "page_title_analysis": seo_analysis.page_title_analysis,
                "page_description_analysis": seo_analysis.page_description_analysis,
                "content_title_analysis": seo_analysis.content_title_analysis,
                "internal_link_analysis": seo_analysis.internal_link_analysis,
                },
            }

        return article_analysis

    def _page_title_report(self, page_title_analysis):
        """
        Create report for page title thanks to dedicated analysis.
        Return a dict with details.
        """

        report = {
            'title': 'Page title analysis',
            'content': {
                'good': [],
                'to_improve': [],
                'problems': [],
            },
        }

        if page_title_analysis.has_page_title:
            report['content']['good'].append('You have declared a title. Nice job !')

            if page_title_analysis.page_title_length in SEOReport.PAGE_TITLE_RECOMMENDED_LENGTH:
                report['content']['good'].append('Your title has a good longer.')

            elif page_title_analysis.page_title_length < SEOReport.PAGE_TITLE_RECOMMENDED_LENGTH[0]:
                report['content']['to_improve'].append('Your title is too short. The recommended length is 70 characters.')
            
            elif page_title_analysis.page_title_length > SEOReport.PAGE_TITLE_RECOMMENDED_LENGTH[-1]:
                report['content']['to_improve'].append('Your title is too long. The maximum recommended length is 70 characters.')

        else:
            report['content']['problems'].append('Title is missing. Create one to improve your SEO.')

        return report

    def _page_description_report(self, page_description_analysis):
        """
        Create report for page description thanks to dedicated analysis.
        Return a dict with details.
        """

        report = {
            'title': 'Page description analysis',
            'content': {
                'good': [],
                'to_improve': [],
                'problems': [],
            },
        }

        if page_description_analysis.has_page_description():
            report['content']['good'].append('You have declared a description. Nice job !')

            if page_description_analysis.page_description_length in SEOReport.PAGE_DESCRIPTION_RECOMMENDED_LENGTH:
                report['content']['good'].append('Your description has a good longer')

            elif page_description_analysis.page_description_length < SEOReport.PAGE_DESCRIPTION_RECOMMENDED_LENGTH[0]:
                report['content']['to_improve'].append('Your description is too short. The minimum recommended length is 150 characters.')
            
            elif page_description_analysis.page_description_length > SEOReport.PAGE_DESCRIPTION_RECOMMENDED_LENGTH[-1]:
                report['content']['to_improve'].append('Your description is too long. The maximum recommended length is 160 characters.')

        else:
            report['content']['problems'].append('You need to declare a description to improve SEO.')

        return report

    def _content_title_report(self, content_title_analysis):
        """
        Create report for content title thanks to dedicated analysis.
        Return a dict with details.
        """

        report = {
            'title': 'Content title analysis',
            'content': {
                'good': [],
                'to_improve': [],
                'problems': [],
            },
        }

        if content_title_analysis.has_content_title():
            report['content']['good'].append('You have declared a content title. Nice job !')

            if not content_title_analysis.is_content_title_unique():
                report['content']['to_improve'].append('Your content title must be unique.')
        else:
            report['content']['problems'].append('You\'re missing a content title.')

        return report

    def _internal_link_report(self, internal_link_analysis):
        """
        Create report for internal links thanks to dedicated analysis.
        Return a dict with details.
        """

        report = {
            'title': 'Internal link analysis',
            'content': {
                'good': [],
                'to_improve': [],
                'problems': [],
            }
        }

        internal_link_occurrence = internal_link_analysis.internal_link_occurrence

        if internal_link_analysis.has_internal_link():
            report['content']['good'].append(
                'You\'ve included ' + str(internal_link_occurrence) + ' internal links. Nice job !'
            )

        else:
            report['content']['problems'].append('It\'s better to include internal links.')

        return report

    def _launch_report(self, article_analysis):
        """
        Get all articles analysis and launch dedicated report for each.
        Return a dict with all micro-reports.
        """

        page_title_analysis = article_analysis['seo_analysis']['page_title_analysis']
        page_description_analysis = article_analysis['seo_analysis']['page_description_analysis']
        content_title_analysis = article_analysis['seo_analysis']['content_title_analysis']
        internal_link_analysis = article_analysis['seo_analysis']['internal_link_analysis']

        page_title_report = self._page_title_report(page_title_analysis)
        page_description_report = self._page_description_report(page_description_analysis)
        content_title_report = self._content_title_report(content_title_analysis)
        internal_link_report = self._internal_link_report(internal_link_analysis)

        article_report = [
            page_title_report,
            page_description_report,
            content_title_report,
            internal_link_report,
        ]

        return article_report

    def generate(self, site_name, articles_analysis):
        """
        Generate the SEO report.
        Return HTML file generated by Jinja2.
        """

        seo_reports = []
        for article_analysis in articles_analysis:

            article_report = self._launch_report(article_analysis)

            articles_reports = {
                'article_url': article_analysis.get('article'),
                'seo_reports': article_report,
                }

            seo_reports.append(articles_reports)

        # Get Jinja HTML template
        plugin_path = os.path.dirname(os.path.realpath(__file__))
        file_loader = FileSystemLoader(plugin_path + '/template')
        env = Environment(loader=file_loader)

        template = env.get_template('seo_report.html')
        css_file = plugin_path + '/static/seo_report.css'
        output = template.render(site_name=site_name, seo_reports=seo_reports, css_file=css_file)

        # Create HTML file
        with open("seo_report.html", 'w') as report:
            report.write(output)
