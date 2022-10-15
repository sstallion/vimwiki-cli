# Contributing

If you have an idea or feature request please open an [issue][1], even if you
don't have time to contribute!

## Making Changes

> **Note**: This guide assumes you have a working Python installation (most
> versions are supported) and have the Python Package Installer available in
> the current user's $PATH.

To get started, [fork][2] this repository on GitHub and clone a working copy for
development:

    $ git clone git@github.com:YOUR-USERNAME/vimwiki-cli.git

Once cloned, change the directory to your working copy, create a new virtual
environment, and activate:

    $ python -m venv venv
    $ source venv/bin/activate

> **Note**: If building for Python 2.7, the `virtualenv` package should be used
> instead, which can be installed locally by issuing `pip install --user virtualenv`.

Dependencies are managed via `setuptools`; to set up the environment for
development, issue:

    $ python -m pip install -e '.[test]'

Once you are finished making changes, be sure to check the output of
`pycodestyle` and `pytest` by issuing:

    $ python -m pycodestyle
    $ python -m pytest

At a minimum, there should be no test regressions and additional tests should be
added for new functionality. If user-facing changes are introduced, be sure add
an entry to the `Unreleased` section in [CHANGELOG.md][3].

Finally, commit your changes and create a [pull request][4] against the `master`
branch for review.

## Making New Releases

Making new releases is automated by GitHub Actions. Releases should only be
created from the `master` branch; as such `master` should be passing tests at
all times.

To make a new release, follow these steps:

1. Install release dependencies by issuing:

       $ python -m pip install -e '.[release]'

2. Increment the version number by issuing:

       $ bump2version <major|minor|patch>

3. Create a new section in [CHANGELOG.md][3] for the new version, and move items
   from `Unreleased` to this section. Links should also be updated to point to
   the correct tags for comparison.

4. Verify release notes by issuing:

       $ python scripts/release_notes.py v<version>

5. Commit outstanding changes by issuing:

       $ git commit -a -m 'Release v<version>'

6. Push changes to the remote repository and verify the results of the [CI][5]
   workflow:

       $ git push origin master

7. Create a release tag by issuing:

       $ git tag -a -m 'Release v<version>' v<version>

8. Push the release tag to the remote repository and verify the results of the
   [Release][6] workflow:

       $ git push origin --tags

## License

By contributing to this repository, you agree that your contributions will be
licensed under its Simplified BSD License.

[1]: https://github.com/sstallion/vimwiki-cli/issues
[2]: https://docs.github.com/en/github/getting-started-with-github/fork-a-repo
[3]: https://github.com/sstallion/vimwiki-cli/blob/master/CHANGELOG.md
[4]: https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request
[5]: https://github.com/sstallion/vimwiki-cli/actions/workflows/ci.yml
[6]: https://github.com/sstallion/vimwiki-cli/actions/workflows/release.yml
