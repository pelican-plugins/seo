"""Units tests for SEO Enhancer."""

from unittest.mock import mock_open, patch

import pytest


class TestSEOEnhancer:
    """Units tests for SEOEnhancer."""

    def test_populate_robots_return_dict_with_rules_for_an_url(
        self, fake_seo_enhancer, fake_article
    ):
        """
        Test that populate_robots return a dict with document_url,
        noindex and disallow rules.
        """

        fake_robots_rules = fake_seo_enhancer.populate_robots(fake_article)

        assert fake_robots_rules["document_url"]
        assert fake_robots_rules["noindex"]
        assert fake_robots_rules["disallow"]

    def test_generate_robots_file(self, fake_seo_enhancer, fake_robots_rules):
        """Test if generate_robots create a robots.txt file by mocking open()."""

        with patch("os.mkdir"):
            with patch("seo.seo_enhancer.open", mock_open()) as mocked_open:
                mocked_file_handle = mocked_open.return_value

                fake_seo_enhancer.generate_robots(
                    rules=fake_robots_rules, output_path="fake_output"
                )

                mocked_open.assert_called_once_with("fake_output/robots.txt", "w+")
                mocked_file_handle.write.assert_called()
                # 4 : 1 fix write + 3 generated write
                assert len(mocked_file_handle.write.call_args_list) == 4

                args, _ = mocked_file_handle.write.call_args_list[1]
                fake_rule = args[0]
                assert "Noindex: fake-title.html" in fake_rule

    @pytest.mark.parametrize("open_graph", (True, False))
    def test_launch_html_enhancer_returns_dict(
        self, fake_article, fake_seo_enhancer, open_graph
    ):
        """
        Test if launch_html_enhancer returns a dict with expected keys.
        :open_graph: is optional.
        """

        fake_html_enhancements = fake_seo_enhancer.launch_html_enhancer(
            file=fake_article,
            output_path="fake_output",
            path="fake_output/fake_file.html",
            open_graph=open_graph,
        )

        assert fake_html_enhancements["canonical_tag"]
        assert fake_html_enhancements["article_schema"]
        assert fake_html_enhancements["breadcrumb_schema"]

        if open_graph:
            assert fake_html_enhancements["open_graph"]
        else:
            assert "open_graph" not in fake_html_enhancements

    def test_add_html_enhancements_to_file(self, fake_article, fake_seo_enhancer):
        """
        Test if add_html_to_file add SEO enhancements
        to HTML files by mocking open().
        """

        path = "fake_output/fake_file.html"
        fake_html_enhancements = fake_seo_enhancer.launch_html_enhancer(
            file=fake_article,
            output_path="fake_output",
            path=path,
        )

        with patch(
            "seo.seo_enhancer.open", mock_open(read_data=fake_article.content)
        ) as mocked_open:
            mocked_file_handle = mocked_open.return_value

            fake_seo_enhancer.add_html_to_file(
                enhancements=fake_html_enhancements, path=path
            )
            assert len(mocked_open.call_args_list) == 2
            mocked_file_handle.read.assert_called_once()
            mocked_file_handle.write.assert_called_once()

            write_args, _ = mocked_file_handle.write.call_args_list[0]
            fake_html_content = write_args[0]

            assert (
                fake_html_content
                == """<html>
<head>
<title>Fake Title</title>
<meta content="Fake description" name="description"/>
<link href="https://www.fakesite.com/fake-title.html" rel="canonical"/>\
<script type="application/ld+json">\
{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Fake Site Name", "item": "https://www.fakesite.com"}, {"@type": "ListItem", "position": 2, "name": "Fake_file", "item": "https://www.fakesite.com/fake_file.html"}]}\
</script>\
<script type="application/ld+json">\
{"@context": "https://schema.org", "@type": "Article", "author": {"@type": "Person", "name": "Fake author"}, "publisher": {"@type": "Organization", "name": "Fake Site Name", "logo": {"@type": "ImageObject", "url": "https://www.fakesite.com/fake-logo.jpg"}}, "headline": "Fake Title", "about": "Fake category", "datePublished": "2019-04-03 23:49"}\
</script>\
</head>
<body>
<h1>Fake content title</h1>
<p>Fake content 🙃</p>
<a href="https://www.fakesite.com">Fake internal link</a>
<p>Fake content with <code>inline code</code></p>
<p>Fake content with "<a href="https://www.fakesite.com">Fake inline internal link</a>"</p>
</body>
</html>"""
            )

    @pytest.mark.parametrize(
        "metadata,expected_tag",
        [
            (
                {},
                '<link href="https://www.fakesite.com/fake-title.html" rel="canonical"/>',
            ),
            (
                {"save_as": "custom_file_name.html"},
                '<link href="https://www.fakesite.com/custom_file_name.html" rel="canonical"/>',
            ),
            (
                {
                    "external_canonical": "https://www.example.com/external_canonical_article.html"
                },
                '<link href="https://www.example.com/external_canonical_article.html" rel="canonical"/>',
            ),
            (
                {
                    "save_as": "custom_file_name.html",
                    "external_canonical": "https://www.example.com/external_canonical_article.html",
                },
                '<link href="https://www.example.com/external_canonical_article.html" rel="canonical"/>',
            ),
        ],
    )
    def test_html_output_with_canonical_url(
        self, fake_article, fake_seo_enhancer, metadata, expected_tag
    ):
        """
        Test the HTML output for canonical url tag according to the article metadata.
        If no metadata are filled, default canonical URL is SITEURL/file_name.
        """
        path = "fake_output/fake_file.html"
        fake_article.metadata.update(metadata)

        fake_html_enhancements = fake_seo_enhancer.launch_html_enhancer(
            file=fake_article,
            output_path="fake_output",
            path=path,
        )

        with patch(
            "seo.seo_enhancer.open", mock_open(read_data=fake_article.content)
        ) as mocked_open:
            mocked_file_handle = mocked_open.return_value

            fake_seo_enhancer.add_html_to_file(
                enhancements=fake_html_enhancements, path=path
            )
            assert len(mocked_open.call_args_list) == 2
            mocked_file_handle.read.assert_called_once()
            mocked_file_handle.write.assert_called_once()

            write_args, _ = mocked_file_handle.write.call_args_list[0]
            fake_html_content = write_args[0]

            assert expected_tag in fake_html_content

    def test_add_html_enhancements_to_file_with_open_graph(
        self, fake_article, fake_seo_enhancer
    ):
        """
        Test if add_html_to_file with open_graph setting
        adds Open Graph tags to HTML files.
        """

        path = "fake_output/fake_file.html"
        fake_html_enhancements = fake_seo_enhancer.launch_html_enhancer(
            file=fake_article,
            output_path="fake_output",
            path=path,
            open_graph=True,
        )

        with patch(
            "seo.seo_enhancer.open", mock_open(read_data=fake_article.content)
        ) as mocked_open:
            mocked_file_handle = mocked_open.return_value

            fake_seo_enhancer.add_html_to_file(
                enhancements=fake_html_enhancements, path=path
            )
            assert len(mocked_open.call_args_list) == 2
            mocked_file_handle.read.assert_called_once()
            mocked_file_handle.write.assert_called_once()

            write_args, _ = mocked_file_handle.write.call_args_list[0]
            fake_html_content = write_args[0]

            assert (
                fake_html_content
                == """<html>
<head>
<title>Fake Title</title>
<meta content="Fake description" name="description"/>
<link href="https://www.fakesite.com/fake-title.html" rel="canonical"/>\
<script type="application/ld+json">\
{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Fake Site Name", "item": "https://www.fakesite.com"}, {"@type": "ListItem", "position": 2, "name": "Fake_file", "item": "https://www.fakesite.com/fake_file.html"}]}\
</script>\
<script type="application/ld+json">\
{"@context": "https://schema.org", "@type": "Article", "author": {"@type": "Person", "name": "Fake author"}, "publisher": {"@type": "Organization", "name": "Fake Site Name", "logo": {"@type": "ImageObject", "url": "https://www.fakesite.com/fake-logo.jpg"}}, "headline": "Fake Title", "about": "Fake category", "datePublished": "2019-04-03 23:49"}\
</script>\
<meta content="https://www.fakesite.com/fake-title.html" property="og:url"/>\
<meta content="website" property="og:type"/>\
<meta content="OG Title" property="og:title"/>\
<meta content="OG Description" property="og:description"/>\
<meta content="https://www.fakesite.com/og-image.jpg" property="og:image"/>\
<meta content="fr_FR" property="og:locale"/>\
</head>
<body>
<h1>Fake content title</h1>
<p>Fake content 🙃</p>
<a href="https://www.fakesite.com">Fake internal link</a>
<p>Fake content with <code>inline code</code></p>
<p>Fake content with "<a href="https://www.fakesite.com">Fake inline internal link</a>"</p>
</body>
</html>"""
            )

    def test_add_html_enhancements_to_file_with_twitter_cards(
        self, fake_article, fake_seo_enhancer
    ):
        """
        Test if add_html_to_file with twitter_cards setting
        adds Twitter Cards tags to HTML files.
        It'll also add Open Graph tags as Twitter Cards feature
        requires them.
        """

        path = "fake_output/fake_file.html"
        fake_html_enhancements = fake_seo_enhancer.launch_html_enhancer(
            file=fake_article,
            output_path="fake_output",
            path=path,
            open_graph=True,
            twitter_cards=True,
        )

        with patch(
            "seo.seo_enhancer.open", mock_open(read_data=fake_article.content)
        ) as mocked_open:
            mocked_file_handle = mocked_open.return_value

            fake_seo_enhancer.add_html_to_file(
                enhancements=fake_html_enhancements, path=path
            )
            assert len(mocked_open.call_args_list) == 2
            mocked_file_handle.read.assert_called_once()
            mocked_file_handle.write.assert_called_once()

            write_args, _ = mocked_file_handle.write.call_args_list[0]
            fake_html_content = write_args[0]

            assert (
                fake_html_content
                == """<html>
<head>
<title>Fake Title</title>
<meta content="Fake description" name="description"/>
<link href="https://www.fakesite.com/fake-title.html" rel="canonical"/>\
<script type="application/ld+json">\
{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Fake Site Name", "item": "https://www.fakesite.com"}, {"@type": "ListItem", "position": 2, "name": "Fake_file", "item": "https://www.fakesite.com/fake_file.html"}]}\
</script>\
<script type="application/ld+json">\
{"@context": "https://schema.org", "@type": "Article", "author": {"@type": "Person", "name": "Fake author"}, "publisher": {"@type": "Organization", "name": "Fake Site Name", "logo": {"@type": "ImageObject", "url": "https://www.fakesite.com/fake-logo.jpg"}}, "headline": "Fake Title", "about": "Fake category", "datePublished": "2019-04-03 23:49"}\
</script>\
<meta content="summary" name="twitter:card"/>\
<meta content="@TestTWCards" name="twitter:site"/>\
<meta content="https://www.fakesite.com/fake-title.html" property="og:url"/>\
<meta content="website" property="og:type"/>\
<meta content="OG Title" property="og:title"/>\
<meta content="OG Description" property="og:description"/>\
<meta content="https://www.fakesite.com/og-image.jpg" property="og:image"/>\
<meta content="fr_FR" property="og:locale"/>\
</head>
<body>
<h1>Fake content title</h1>
<p>Fake content 🙃</p>
<a href="https://www.fakesite.com">Fake internal link</a>
<p>Fake content with <code>inline code</code></p>
<p>Fake content with "<a href="https://www.fakesite.com">Fake inline internal link</a>"</p>
</body>
</html>"""
            )
