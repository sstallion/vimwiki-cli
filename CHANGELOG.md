# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `pre-commit` hook `id: vimwiki-cli` to simplify installing `pre-commit.sh`
  script (
  [Issue #7](https://github.com/sstallion/vimwiki-cli/issues/7#issue-876664886))

### Changed

- Github Actions workflow `CI` removed python-2.7 and added python-3.11 because
  `ubuntu-latest` dropped python-2.7 support. Updated `checkout` and
  `setup-python` actions to latest versions.

## [v1.1.0] - 2023-05-08

### Added

- Add support for `VimwikiAll2HTML[!]` ([jfishe](https://github.com/jfishe))

### Changed

- Update documentation
- Add `vimwiki.allhtml` to `scripts/pre-commit.sh`

## [v1.0.2] - 2022-09-04

### Changed

- Fix PyPI documentation

## [v1.0.1] - 2022-09-04

### Added

- Add support for Python 3.10

### Changed

- Update documentation
- Update Click dependency to `>=7.1` ([Anish Lakhwara](https://github.com/Chickensoupwithrice))

### Removed

- Remove support for Python 3.6

## [v1.0.0] - 2021-05-04

Initial release

[Unreleased]: https://github.com/sstallion/vimwiki-cli/compare/v1.1.0...HEAD
[v1.1.0]: https://github.com/sstallion/vimwiki-cli/releases/tag/v1.1.0
[v1.0.2]: https://github.com/sstallion/vimwiki-cli/releases/tag/v1.0.2
[v1.0.1]: https://github.com/sstallion/vimwiki-cli/releases/tag/v1.0.1
[v1.0.0]: https://github.com/sstallion/vimwiki-cli/releases/tag/v1.0.0
