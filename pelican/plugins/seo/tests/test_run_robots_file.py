from seo.seo import run_robots_file
import pytest
from unittest.mock import patch, call, MagicMock


def test_run_robots_file():
    class FakeGenerator:
        context = {
            "SEO_ENHANCER": True,
            "SEO_ENHANCER_SITEMAP_URL": "https://www.example.com/sitemap.xml",
        }
        output_path = "foo"

    with patch("seo.seo.SEOEnhancer") as patched_seo_enhancer:
        run_robots_file([FakeGenerator()])

        assert (
            call().generate_robots(
                rules=[],
                output_path="foo",
                sitemap_url="https://www.example.com/sitemap.xml",
            )
            in patched_seo_enhancer.mock_calls
        )
