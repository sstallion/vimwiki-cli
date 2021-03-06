# Vimwiki Command-Line Interface

[![](https://img.shields.io/travis/com/sstallion/vimwiki-cli)][1]
[![](https://img.shields.io/pypi/v/vimwiki-cli)][2]
[![](https://img.shields.io/pypi/pyversions/vimwiki-cli)][2]
[![](https://img.shields.io/github/license/sstallion/vimwiki-cli)][LICENSE]

`vimwiki-cli` is a command-line interface to [Vimwiki][3], a plugin for the
[Vim][4] text editor. It provides a front-end for interactive editor commands
and can be used to automate repetitive tasks such as rebuilding tag metadata and
generating links, all from the command line.

[![](https://asciinema.org/a/413921.svg)](https://asciinema.org/a/413921?autoplay=1)

## Installation

`vimwiki-cli` is available on [PyPI][2] and can be installed locally using the
Python Package Installer:

    $ pip install --user vimwiki-cli

Once installed, issue `vimwiki --help` to see usage.

## Configuration

For most installations no configuration is needed, however several environment
variables are available to modify default behavior without the need to pass
global options on the command line:

| Environment Variable   | Global Option    | Description                                       |
|------------------------|------------------|---------------------------------------------------|
| `VIMWIKI_EDITOR`       | `--editor`       | Editor to launch, defaults to `$EDITOR` or `vim`. |
| `VIMWIKI_COUNT`        | `--count`        | Index of wiki to open.                            |
| `VIMWIKI_SELECT`       | `--select`       | Select wiki from interactive list.                |
| `VIMWIKI_OPEN_MATCHES` | `--open-matches` | Open search results by default.                   |
| `VIMWIKI_OPEN_TABS`    | `--open-tabs`    | Open pages in a new tab by default.               |

## Advanced

### Supported Commands

Each CLI command corresponds to one or more Ex commands executed in the editor.
The following table details the mapping between these commands:

| CLI Command                             | Ex Commands                                                         |
|-----------------------------------------|---------------------------------------------------------------------|
| `vimwiki`                               | `:VimwikiIndex`                                                     |
| `vimwiki check-links`                   | `:VimwikiIndex \| VimwikiCheckLinks`                                |
| `vimwiki diary`                         | `:VimwikiDiaryIndex`                                                |
| `vimwiki diary generate-links`          | `:VimwikiDiaryIndex \| VimwikiDiaryGenerateLinks`                   |
| `vimwiki diary today`                   | `:VimwikiMakeDiaryNote`                                             |
| `vimwiki diary tomorrow`                | `:VimwikiMakeTomorrowDiaryNote`                                     |
| `vimwiki diary yesterday`               | `:VimwikiMakeYesterdayDiaryNote`                                    |
| `vimwiki generate-links PAGE PATTERN`   | `:VimwikiIndex \| VimwikiGoto PAGE \| VimwikiGenerateLinks PATTERN` |
| `vimwiki goto PAGE`                     | `:VimwikiIndex \| VimwikiGoto PAGE`                                 |
| `vimwiki help`                          | `:help vimwiki.txt \| only`                                         |
| `vimwiki search PATTERN`                | `:VimwikiIndex \| VimwikiSearch PATTERN`                            |
| `vimwiki tags generate-links PAGE TAGS` | `:VimwikiIndex \| VimwikiGoto PAGE \| VimwikiGenerateTagLinks TAGS` |
| `vimwiki tags rebuild`                  | `:VimwikiIndex \| VimwikiRebuildTags`                               |
| `vimwiki tags search PATTERN`           | `:VimwikiIndex \| VimwikiSearchTags PATTERN`                        |

### Shell Completion

Shell completion is available for `bash`, `fish`, and `zsh` shells. To generate
an activation script, issue:

    $ env _VIMWIKI_COMPLETE=source_$(basename $SHELL) vimwiki >/path/to/vimwiki-complete.sh

Once generated, the activation script may be sourced directly or from the shell
startup file to provide completion:

    $ . /path/to/vimwiki-complete.sh

### Git Integration

For wikis managed with Git, a pre-commit hook script is available that executes
non-interactive commands to rebuild tag metadata and generate links before
commit.

The pre-commit hook relies on the following configuration options:

| Configuration Option          | Description                                    |
|-------------------------------|------------------------------------------------|
| `vimwiki.options`             | Extra options to pass to the `vimwiki` command |
| `vimwiki.linkspage`           | Page which contains generated links            |
| `vimwiki.taglinkspage`        | Page which contains generated tag links        |
| `vimwiki.generatelinks`       | Generate links before commit (bool)            |
| `vimwiki.generatediarylinks`  | Generate diary links before commit (bool)      |
| `vimwiki.generatetaglinks`    | Generate tag links before commit (bool)        |
| `vimwiki.rebuildtags`         | Rebuild tag metadata before commit (bool)      |

For example, to configure the hook to rebuild tag metadata and generate tag
links in the `Tags` page before commit, issue:

    $ git config vimwiki.taglinkspage Tags
    $ git config vimwiki.generatetaglinks true
    $ git config vimwiki.rebuildtags true

To enable the hook, copy or link [pre-commit.sh] to `.git/hooks/pre-commit` in
the wiki directory.

## Contributing

Pull requests are welcome! See [CONTRIBUTING.md] for more details.

## License

Source code in this repository is licensed under a Simplified BSD License. See
[LICENSE] for more details.

[1]: https://travis-ci.com/sstallion/vimwiki-cli
[2]: https://pypi.org/project/vimwiki-cli/
[3]: https://vimwiki.github.io/
[4]: https://www.vim.org/

[CONTRIBUTING.md]: CONTRIBUTING.md
[LICENSE]: LICENSE
[pre-commit.sh]: scripts/pre-commit.sh
