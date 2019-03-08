class PageTitleAnalyzer():

    def __init__(self, metadata):
        self.metadata = metadata

    def has_page_title(self, metadata):
        if self.metadata.get('title'):
            return True
