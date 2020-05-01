""" Units tests for SEO Enhancer. """

from unittest.mock import mock_open, patch


class TestSEOEnhancer():
    """ Units tests for SEOEnhancer. """

    def test_populate_robots_return_dict_with_rules_for_an_url(
            self, fake_seo_enhancer, fake_article):
        """
        Test that populate_robots return a dict with document_url,
        noindex and disallow rules.
        """

        fake_robots_rules = fake_seo_enhancer.populate_robots(fake_article)

        assert fake_robots_rules['document_url']
        assert fake_robots_rules['noindex']
        assert fake_robots_rules['disallow']

    def test_generate_robots_file(self, fake_seo_enhancer, fake_robots_rules):
        """ Test if generate_robots create a robots.txt file by mocking open(). """

        with patch('os.mkdir'):
            with patch('seo.seo_enhancer.open', mock_open()) as mocked_open:
                mocked_file_handle = mocked_open.return_value

                fake_seo_enhancer.generate_robots(
                    rules=fake_robots_rules,
                    output_path='fake_output'
                )

                mocked_open.assert_called_once_with('fake_output/robots.txt', 'w+')
                mocked_file_handle.write.assert_called()
                # 4 : 1 fix write + 3 generated write
                assert len(mocked_file_handle.write.call_args_list) == 4

                args, _ = mocked_file_handle.write.call_args_list[1]
                fake_rule = args[0]
                assert "Noindex: fake-title.html" in fake_rule

    def test_launch_html_enhancemer_returns_dict(self, fake_article, fake_seo_enhancer):
        """ Test if launch_html_enhancemer returns a dict with expected keys. """

        fake_html_enhancements = fake_seo_enhancer.launch_html_enhancer(
            file=fake_article,
            output_path='fake_output',
            path='fake_dir/fake_output/fake_file.html',
        )

        assert fake_html_enhancements['canonical_tag']
        assert fake_html_enhancements['article_schema']
        assert fake_html_enhancements['breadcrumb_schema']

    def test_add_html_enhancements_to_file(self, fake_article, fake_seo_enhancer):
        """
        Test if add_html_to_file add SEO enhancements
        to HTML files by mocking open().
        """

        path = "fake_dir/fake_output/fake_file.html"
        fake_html_enhancements = fake_seo_enhancer.launch_html_enhancer(
            file=fake_article,
            output_path='fake_output',
            path=path,
        )

        with patch(
            'seo.seo_enhancer.open',
            mock_open(read_data=fake_article.content)
        ) as mocked_open:
            mocked_file_handle = mocked_open.return_value

            fake_seo_enhancer.add_html_to_file(
                enhancements=fake_html_enhancements,
                path=path
            )
            assert len(mocked_open.call_args_list) == 2
            mocked_file_handle.read.assert_called_once()
            mocked_file_handle.write.assert_called_once()

            write_args, _ = mocked_file_handle.write.call_args_list[0]
            fake_html_content = write_args[0]
            assert '<link href="fakesite.com/fake-title.html" rel="canonical"/>' \
                in fake_html_content
            assert '{"@context": "https://schema.org", "@type": "Article"' \
                in fake_html_content
            assert '{"@context": "https://schema.org", "@type": "BreadcrumbList"' \
                in fake_html_content
