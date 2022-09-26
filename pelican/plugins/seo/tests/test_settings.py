from seo import get_plugin_settings


def test_get_settings():
    """
    Settings are filled from:
    - firstly by plugin settings file
    - secondly by Pelican settings file, which will override the first one
    """
    pelican_context = {"SEO_TEST": True, "SETTING": "FAKE", "SEO_FAKE": False}

    settings = get_plugin_settings(context=pelican_context)

    assert (
        len(settings) == 8
    )  # 6 in the plugin settings file + 2 from the Pelican context

    # Let's define a setting in Pelican context that
    # override the identic plugin setting value
    assert settings["SEO_REPORT"] is True

    settings = get_plugin_settings(context={"SEO_REPORT": False})

    assert len(settings) == 6
    assert settings["SEO_REPORT"] is False
