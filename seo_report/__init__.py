"""
Generate a SEO report by calling SEO analyzers for each content.
"""

from .seo_analyzer import SEOAnalyzer

class SEOReport():
    """ Generate a SEO report by calling SEO analyzers for each content. """

    PAGE_TITLE_RECOMMENDED_LENGTH = range(70, 76)
    PAGE_DESCRIPTION_RECOMMENDED_LENGTH = range(150, 161)

    def __init__(self, metadata):
        self.seo_analysis = SEOAnalyzer(metadata)

    def page_title_report(self):
        """ Create report for page title. """

        if self.seo_analysis.page_title_analysis.has_page_title:
            print("SEO : You have declared a title. Nice job !")

            if self.seo_analysis.page_title_analysis.page_title_length in SEOReport.PAGE_TITLE_RECOMMENDED_LENGTH:
                print("SEO : Your title has a good longer")
            else:
                print("SEO : Your title is too short or too long. The recommended length is between characters.")

        else:
            print("SEO : You need to declare a title to improve SEO")

    def page_description_report(self):
        """ Create report for page description. """

        if self.seo_analysis.page_description_analysis.has_page_description():
            print("SEO : You have declared a description. Nice job !")

            if self.seo_analysis.page_description_analysis.page_description_length in SEOReport.PAGE_DESCRIPTION_RECOMMENDED_LENGTH:
                print("SEO : Your description has a good longer")
            else:
                print("SEO : Your description is too short or too long. The recommended length is between characters.")

        else:
            print("SEO : You need to declare a description to improve SEO")

