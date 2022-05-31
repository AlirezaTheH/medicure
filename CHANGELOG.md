# Changelog
All notable changes to this project will be documented in this file.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]
### Added
- Enabled direct subtitle injecting when treating media
- Added pre-commit ci for auto updating pre-commit hooks
- Medicure now keeps actions up to date with Dependabot

### Changed
- Treated movies and subtitles are now being created in a different directory
  from the original files.

### Fixed
- Fixed a bug in extracting track info from subtitle files
- Fixed `mkvmerge`'s `--no-subtitles` flag when dubbing supplier has no subtitle
  tracks
- Fixed a bug in extracting `track_id` from subtitle files

## [0.1.5] - 2022-05-28
### Added
- Added [BumpVer](https://github.com/mbarkhau/bumpver) config
- Add extras requirements
- Added `CODE_OF_CONDUCT.md`
- Added `CHANGELOG.md`
- Added PyPI labels to `README.md`

### Changed
- Reformatted `CHANGELOG.md` to
  [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format
- Improved media and subtitle patterns
- Improved typer patch speed

### Fixed
- Add `MANIFEST.in` to include extras requirements in source builds
- Remove unnecessary exclusion from `pre-commit` excludes
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


[Unreleased]: https://github.com/alirezatheh/medicure/compare/v0.1.5...HEAD
[0.1.5]: https://github.com/alirezatheh/medicure/compare/v0.0.4...v0.1.5
[0.0.4]: https://github.com/alirezatheh/medicure/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/alirezatheh/medicure/releases/tag/v0.0.3
