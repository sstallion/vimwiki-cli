# Contributing

If you have an idea or feature request please open an [issue], even if you don't
have time to contribute!

## Making Changes

> **Note**: This guide assumes you have a working Python installation (most
> versions are supported) and have the Python Package Installer available in
> your PATH.

To get started, [fork] this repository on GitHub and clone a working copy for
development:

    $ git clone git@github.com:YOUR-USERNAME/vimwiki-cli.git

Once cloned, change the directory to your working copy, create a new virtualenv,
and activate the environment:

    $ virtualenv venv
    $ source venv/bin/activate

> **Note**: If the `virtualenv` command is not available, it can be installed
> locally by issuing `pip install --user virtualenv`.

Dependencies are managed via `setuptools`; to set up the environment for
development, issue:

    $ pip install -e ".[test]"

Once you are finished making changes, be sure to check the output of
`pycodestyle` and `pytest`. At a minimum, there should be no test regressions
and additional tests should be added for new functionality. If user-facing
changes are introduced, be sure add an entry to the `Unreleased` section in
[CHANGELOG.md] as well.

With that out of the way, you can now commit your changes and create a [pull
request] against the `master` branch for review!

## Making New Releases

Making new releases is automated by the Travis CI deployment pipeline. Releases
should only be created from the `master` branch; as such `master` should be
passing tests at all times.

To make a new release, follow these steps:

1. Install dependencies by issuing `pip install -e ".[deploy]"` in an existing
   virtualenv (see above).
2. Verify `pycodestyle` and `pytest` are passing locally.
3. Increment the version number by issuing `bump2version <major|minor|patch>`.
4. Create a new section in [CHANGELOG.md] for the new version, and move items
   from `Unreleased` to this section. Links should also be updated to point to
   the correct tags for comparisons.
5. Verify release notes by issuing `scripts/release_notes.py v<version>` and
   make adjustments as needed.
6. Commit changes by issuing `git commit -a -m "Release v<version>"`.
7. Create a release tag by issuing `git tag -a -m "Release v<version>"
   v<version>`.
8. Push changes to `master` by issuing `git push origin master --tags`.
9. Verify Travis CI deploys successfully to PyPI and GitHub.

## License

By contributing to this repository, you agree that your contributions will be
licensed under its Simplified BSD License.

[CHANGELOG.md]: https://github.com/sstallion/vimwiki-cli/blob/master/CHANGELOG.md
[fork]: https://docs.github.com/en/github/getting-started-with-github/fork-a-repo
[issue]: https://github.com/sstallion/vimwiki-cli/issues
[pull request]: https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request
