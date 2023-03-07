# Changelog
All notable changes to this project will be documented in this file.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]
### Added
- Added Medicure's documentation
- Added support for Python `3.11`
- Added Rich integration to beatify CLI outputs

### Fixed
- Removed type hints from docstrings
- Adjusted CLI tests with Rich integration
- Fixed Typer's patch issue with PyPI


## [0.2.0] - 2022-06-15
### Added
- Added pre-commit ci support
- Added Codecov support
- Added CLI tests
- Added TMDB mocks to minimize tests' runtime
- Added `to_list` and `to_dict` converters to `DubbingSupplier` so can be
  easily used in Medicure's CLI
- Added tests workflow
- Added treat tests
- Enabled direct subtitle injecting when treating media
- Added pre-commit ci for auto updating pre-commit hooks
- Medicure now keeps actions up to date with Dependabot

### Changed
- Updated Medicure's CLI base path for all platforms
- Improved tests' parameterizing
- Changed Typer patch method to use pure patch files
- Improved treat tests code coverage
- Improved extracting episode number from file names
- Improved saving file tracks' info
- Improved pip caching in publish workflow
- Treated subtitle files when `include_full_information` is `False`, now will
  be copied to destination directory before renaming.
- Treated movies and subtitles are now being created in a different directory
  from the original files.

### Fixed
- Fixed Typer patch bug in Windows
- Fixed a bug in treating `.sub` files
- Fixed CLI's error messages
- Fixed publish workflow's pip caching
- Fixed a bug in extracting release year for movies
- Fixed a bug in extracting track info from subtitle files
- Fixed `mkvmerge`'s `--no-subtitles` flag when dubbing supplier has no subtitle
  tracks
- Fixed a bug in extracting `track_id` from subtitle files


## [0.1.5] - 2022-05-28
### Added
- Added [BumpVer](https://github.com/mbarkhau/bumpver) config
- Added extras requirements
- Added `CODE_OF_CONDUCT.md`
- Added `CHANGELOG.md`
- Added PyPI labels to `README.md`

### Changed
- Reformatted `CHANGELOG.md` to
  [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format
- Improved media and subtitle patterns
- Improved Typer patch speed

### Fixed
- Added `MANIFEST.in` to include extras requirements in source builds
- Removed unnecessary exclusion from `pre-commit` excludes
- Set minimum Python version to `3.8`


## [0.0.4] - 2022-05-13
### Added
- Added Medicure to PyPI

### Fixed
- Removed direct dependencies


## [0.0.3] - 2022-05-14
### Added
- Added First version of Python package added
- First version of CLI added


[Unreleased]: https://github.com/alirezatheh/medicure/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/alirezatheh/medicure/compare/v0.1.5...v0.2.0
[0.1.5]: https://github.com/alirezatheh/medicure/compare/v0.0.4...v0.1.5
[0.0.4]: https://github.com/alirezatheh/medicure/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/alirezatheh/medicure/releases/tag/v0.0.3
