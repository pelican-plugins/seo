from .seo_analyzer import SEOAnalyzer

class SEOReport():
    """ """

    PAGE_TITLE_RECOMMENDED_LENGTH = range(74, 80)
    PAGE_DESCRIPTION_RECOMMENDED_LENGTH = range(159, 200)

    def __init__(self, metadata):
        self.seo_analysis = SEOAnalyzer(metadata)

    def page_title_report(self):
        if self.seo_analysis.page_title_analysis.has_page_title:
            print("SEO : You have declared a title. Nice job !")
        else:
            print("SEO : You need to declare a title to improve SEO")

    def page_description_report(self):
        if self.seo_analysis.page_description_analysis.has_page_description:
            print("SEO : You have declared a description. Nice job !")
        else:
            print("SEO : You need to declare a description to improve SEO")
