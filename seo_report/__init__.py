"""
Generate a SEO report by calling SEO analyzers for each content.
"""

from .seo_analyzer import SEOAnalyzer

class SEOReport():
    """ Generate a SEO report by calling SEO analyzers for each content. """

    PAGE_TITLE_RECOMMENDED_LENGTH = range(70, 76)
    PAGE_DESCRIPTION_RECOMMENDED_LENGTH = range(150, 161)

    def __init__(self, article):
        self.seo_analysis = SEOAnalyzer(article)

    def page_title_report(self):
        """ Create report for page title. """

        print("PAGE TITLE REPORT")

        if self.seo_analysis.page_title_analysis.has_page_title:
            print("You have declared a title. Nice job !")

            if self.seo_analysis.page_title_analysis.page_title_length in SEOReport.PAGE_TITLE_RECOMMENDED_LENGTH:
                print("Your title has a good longer")
            else:
                print("Your title is too short or too long. The recommended length is between characters.")

        else:
            print("You need to declare a title to improve SEO")

    def page_description_report(self):
        """ Create report for page description. """

        print("PAGE DESCRIPTION REPORT")

        if self.seo_analysis.page_description_analysis.has_page_description():
            print("You have declared a description. Nice job !")

            if self.seo_analysis.page_description_analysis.page_description_length in SEOReport.PAGE_DESCRIPTION_RECOMMENDED_LENGTH:
                print("Your description has a good longer")
            else:
                print("Your description is too short or too long. The recommended length is between characters.")

        else:
            print("You need to declare a description to improve SEO")

    def content_title_report(self):
        """ Create report for content title. """

        print("CONTENT TITLE REPORT")

        if self.seo_analysis.content_title_analysis.has_content_title():
            print("You have declared a content title <h1>. Nice job !")

            if not self.seo_analysis.content_title_analysis.is_content_title_unique():
                print("But your content title must be unique.")
        else:
            print("You're missing a content title <h1>.")

    def internal_link_report(self):
        """ """

        print("INTERNAL LINK REPORT")
        if self.seo_analysis.internal_link_analysis.has_internal_link():
            print("You've included internal links. Nice job !")

            print(self.seo_analysis.internal_link_analysis.internal_link_occurence)

        else:
            print("It's better to include internal links.")

    # def generate(self):
    #     """ Generate the SEO report. Return string in console. """

    #     self.page_title_report = self._page_title_report()