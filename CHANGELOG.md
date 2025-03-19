CHANGELOG
=========

1.3.1 - 2025-03-19
------------------

Support `SITEURL` values that contain slugs after the domain

Contributed by [Max Pfeiffer](https://github.com/max-pfeiffer) via [PR #74](https://github.com/pelican-plugins/seo/pull/74/)


1.3.0 - 2025-01-15
------------------

- Add ability to configure the plugin via the Pelican settings file

1.2.2 - 2021-06-21
------------------

Improve test for canonical feature and update linters.

1.2.1 - 2021-05-16
------------------

Fix addition of undesirable white space in HTML because of BeautifulSoup.prettify()

1.2.0 - 2021-04-14
------------------

Add support for external canonical URL. Refs #33.

1.1.0 - 2021-03-12
------------------

Open Graph and Twitter Cards support

1.0.3 - 2020-11-15
------------------

Fix definitively encoding issues when open file

1.0.2 - 2020-11-03
------------------

Fix schemas generated in wrong script tags

1.0.1 - 2020-10-30
------------------

* Canonical URL must take into account save_as metadata
* Fix breadcrumb built according to output path
* New test was not taking care of PurePath
* Test unicode encoding and fix linting
* Remove Python code encoding hints
* Force real-path normalization to allow for relative resolution
* Refactor duplicated code

1.0.0 - 2020-08-21
------------------

Initial release as namespace plugin
