""" Units tests for SEO Enhancer. """

from unittest.mock import mock_open, patch


class TestHTMLContent:
    def test_proper_code_tag_generation(
        self, fake_article_with_multiple_inline_elements, fake_seo_enhancer
    ):
        """
        Tests if no whitespace is inserted inside <code> tag.
        """

        path = "fake_output/fake_file.html"
        fake_html_enhancements = fake_seo_enhancer.launch_html_enhancer(
            file=fake_article_with_multiple_inline_elements,
            output_path="fake_output",
            path=path,
            open_graph=True,
            twitter_cards=True,
        )

        with patch(
            "seo.seo_enhancer.open",
            mock_open(read_data=fake_article_with_multiple_inline_elements.content),
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

            assert "<code>an inline code</code>" in fake_html_content
            assert '"<a href="http://cool.site/">cool site</a>"' in fake_html_content
