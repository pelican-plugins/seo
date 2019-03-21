"""
Generate a SEO report by calling SEO analyzers for each content.
"""

from .seo_analyzer import SEOAnalyzer

class SEOReport():
    """ Generate a SEO report by calling SEO analyzers for each content. """

    PAGE_TITLE_RECOMMENDED_LENGTH = range(70, 76)
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
        """ Create report for page title. """

        report = {
            'title': 'Page title analysis'
        }

        if page_title_analysis.has_page_title:
            report['has_title'] = 'You have declared a title. Nice job !'

            if page_title_analysis.page_title_length in SEOReport.PAGE_TITLE_RECOMMENDED_LENGTH:
                report['title_length'] = 'Your title has a good longer'

            else:
                report['title_length'] = 'Your title is too short or too long. The recommended length is between characters.'

        else:
            report['has_title'] = 'You need to declare a title to improve SEO'

        return report

    def _page_description_report(self, page_description_analysis):
        """ Create report for page description. """

        report = {
            'title': 'PAGE DESCRIPTION REPORT'
        }

        if page_description_analysis.has_page_description():
            report['has_page_description'] = 'You have declared a description. Nice job !'

            if page_description_analysis.page_description_length in SEOReport.PAGE_DESCRIPTION_RECOMMENDED_LENGTH:
                report['page_description_length'] = 'Your description has a good longer'
            else:
                report['page_description_length'] = 'Your description is too short or too long. The recommended length is between characters.'

        else:
            report['has_page_description'] = 'You need to declare a description to improve SEO'

        return report

    def _content_title_report(self, content_title_analysis):
        """ Create report for content title. """

        report = {
            'title': 'Content title report'
        }

        if content_title_analysis.has_content_title():
            report['has_content_title'] = 'You have declared a content title <h1>. Nice job !'

            if not content_title_analysis.is_content_title_unique():
                report['is_content_title_unique'] = 'But your content title must be unique.'
        else:
            report['has_content_title'] = 'You\'re missing a content title <h1>.'

        return report

    def _internal_link_report(self, internal_link_analysis):
        """ """

        report = {
            'title': 'Internal link report'
        }

        if internal_link_analysis.has_internal_link():
            report['has_internal_link'] = 'You\'ve included internal links. Nice job !'

            report['internal_link_occurence'] = internal_link_analysis.internal_link_occurence

        else:
            report['has_internal_link'] = 'It\'s better to include internal links.'

        return report

    def _launch_report(self, article_analysis):
        """ """

        page_title_analysis = article_analysis['seo_analysis']['page_title_analysis']
        page_description_analysis = article_analysis['seo_analysis']['page_description_analysis']
        content_title_analysis = article_analysis['seo_analysis']['content_title_analysis']
        internal_link_analysis = article_analysis['seo_analysis']['internal_link_analysis']

        page_title_report = self._page_title_report(page_title_analysis)
        page_description_report = self._page_description_report(page_description_analysis)
        content_title_report = self._content_title_report(content_title_analysis)
        internal_link_report = self._internal_link_report(internal_link_analysis)

        article_report = {
            "seo_report": {
                "page_title_report": page_title_report,
                "page_description_report": page_description_report,
                "content_title_report": content_title_report,
                "internal_link_report": internal_link_report,
            }
        }

        return article_report

    def generate(self, articles_analysis):
        """ Generate the SEO report. Return string in console. """

        seo_report = []
        for article_analysis in articles_analysis:

            report = self._launch_report(article_analysis)

            article_report = {
                'article ': article_analysis.get('article'),
                'seo_reports': report,
                }

            seo_report.append(article_report)

        print(seo_report)

        html_template = """
            <html>
                <header>
                    <title>SEO Report - Pelican SEO</title>
                </header>
                <body>
                    <h1>Votre report SEO</h1>
                    <h2>Analyse du titre de la page</h2>
                </body>
            </html>
        """

        with open("seo_report.html", 'w') as report:
            report.write(html_template)

