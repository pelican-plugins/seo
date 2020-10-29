Release type: patch

* Canonical URL must take into account save_as metadata
* Fix breadcrumb built according to output path
* New test was not taking care of PurePath
* Test unicode encoding and fix linting
* Remove Python code encoding hints
* Force real-path normalization to allow for relative resolution
* Refactor duplicated code