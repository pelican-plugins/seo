class PageDescriptionAnalyzer():

    def __init__(self, metadata):
        self.metadata = metadata

    def has_page_description(self):
        if self.metadata.get('description'):
            return True
