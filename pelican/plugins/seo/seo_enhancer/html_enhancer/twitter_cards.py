class TwitterCards:
    """Add specific Twitter tags according to
    https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/summary.
    Missing tags are filled by Open Graph feature as Twitter falls back on it.
    """

    def __init__(self, tw_account) -> None:
        self.tw_account = tw_account

    def create_tags(self) -> dict:
        """Compute all Twitter Cards elements and return them in a ready-to-use dict."""
        twitter_tags = {}

        twitter_tags["card"] = "summary"

        if self.tw_account:
            twitter_tags["site"] = self.tw_account

        return twitter_tags
