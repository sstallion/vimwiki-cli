# Copyright (C) 2021 Steven Stallion <sstallion@gmail.com>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import mock
import pytest
from click.testing import CliRunner

from vimwiki_cli.__main__ import *
from vimwiki_cli.wiki import Wiki


@pytest.fixture
def runner():
    return CliRunner()


@mock.patch('vimwiki_cli.__main__.make_wiki')
@mock.patch('vimwiki_cli.__main__.index')
@pytest.mark.parametrize('args,expected', [
    ('--editor EDITOR', {'editor': 'EDITOR'}),
    ('--count 42', {'count': 42}),
    ('--select', {'select': True}),
    ('--open-matches', {'open_matches': True}),
    ('--open-tabs', {'open_tabs': True})
])
def test_options(_, mock_make_wiki, runner, args, expected):
    result = runner.invoke(cli, args=args)
    assert result.exit_code == 0

    for key, value in expected.items():
        assert key in mock_make_wiki.call_args.kwargs and \
            mock_make_wiki.call_args.kwargs[key] == value


@mock.patch('vimwiki_cli.__main__.make_wiki')
@mock.patch('vimwiki_cli.__main__.index')
@pytest.mark.parametrize('expected', [
    ({'editor': Wiki.DEFAULT_EDITOR}),
    ({'count': Wiki.DEFAULT_COUNT}),
    ({'select': Wiki.DEFAULT_SELECT}),
    ({'open_matches': Wiki.DEFAULT_OPEN_MATCHES}),
    ({'open_tabs': Wiki.DEFAULT_OPEN_TABS})
])
def test_options_with_defaults(_, mock_make_wiki, runner, expected):
    result = runner.invoke(cli)
    assert result.exit_code == 0

    for key, value in expected.items():
        assert key in mock_make_wiki.call_args.kwargs and \
            mock_make_wiki.call_args.kwargs[key] == value


@mock.patch('vimwiki_cli.__main__.make_wiki')
@mock.patch('vimwiki_cli.__main__.index')
@pytest.mark.parametrize('env,expected', [
    ({'VIMWIKI_EDITOR': 'EDITOR'}, {'editor': 'EDITOR'}),
    ({'VIMWIKI_COUNT': '42'}, {'count': 42}),
    ({'VIMWIKI_SELECT': '1'}, {'select': True}),
    ({'VIMWIKI_OPEN_MATCHES': '1'}, {'open_matches': True}),
    ({'VIMWIKI_OPEN_TABS': '1'}, {'open_tabs': True})
])
def test_options_with_env(_, mock_make_wiki, runner, env, expected):
    result = runner.invoke(cli, env=env)
    assert result.exit_code == 0

    for key, value in expected.items():
        assert key in mock_make_wiki.call_args.kwargs and \
            mock_make_wiki.call_args.kwargs[key] == value


@mock.patch('vimwiki_cli.__main__.index')
def test_default(mock_index, runner):
    result = runner.invoke(cli)
    assert result.exit_code == 0

    # index() should be invoked if no command is specified:
    mock_index.assert_called_with()


@mock.patch('vimwiki_cli.wiki.Wiki.all_html')
@pytest.mark.parametrize('args,expected', [
    ('', False),
    ('--all', True)
])
def test_all_html(mock_all_html, runner, args, expected):
    result = runner.invoke(cli, 'all-html ' + args)
    assert result.exit_code == 0

    mock_all_html.assert_called_with(expected)


@mock.patch('vimwiki_cli.wiki.Wiki.check_links')
def test_check_links(mock_check_links, runner):
    result = runner.invoke(cli, 'check-links')
    assert result.exit_code == 0

    mock_check_links.assert_called_with()


@mock.patch('vimwiki_cli.wiki.Wiki.generate_links')
@pytest.mark.parametrize('args,expected', [
    ('PAGE', ('PAGE', '')),
    ('PAGE PATTERN', ('PAGE', 'PATTERN'))
])
def test_generate_links(mock_generate_links, runner, args, expected):
    result = runner.invoke(cli, 'generate-links ' + args)
    assert result.exit_code == 0

    mock_generate_links.assert_called_with(*expected)


@mock.patch('vimwiki_cli.wiki.Wiki.generate_links')
def test_generate_links_with_empty_page(mock_generate_links, runner):
    result = runner.invoke(cli, 'generate-links ""')
    assert result.exit_code != 0

    mock_generate_links.assert_not_called()


@mock.patch('vimwiki_cli.wiki.Wiki.goto')
def test_goto(mock_goto, runner):
    result = runner.invoke(cli, 'goto PAGE')
    assert result.exit_code == 0

    mock_goto.assert_called_with('PAGE')


@mock.patch('vimwiki_cli.wiki.Wiki.goto')
def test_goto_with_empty_page(mock_goto, runner):
    result = runner.invoke(cli, 'goto ""')
    assert result.exit_code != 0

    mock_goto.assert_not_called()


@mock.patch('vimwiki_cli.wiki.Wiki.help')
def test_help(mock_help, runner):
    result = runner.invoke(cli, 'help')
    assert result.exit_code == 0

    mock_help.assert_called_with()


@mock.patch('vimwiki_cli.wiki.Wiki.index')
def test_index(mock_index, runner):
    result = runner.invoke(cli, 'index')
    assert result.exit_code == 0

    mock_index.assert_called_with()


@mock.patch('vimwiki_cli.wiki.Wiki.search')
def test_search(mock_search, runner):
    result = runner.invoke(cli, 'search PATTERN')
    assert result.exit_code == 0

    mock_search.assert_called_with('PATTERN')


@mock.patch('vimwiki_cli.wiki.Wiki.search')
def test_search_with_empty_pattern(mock_search, runner):
    result = runner.invoke(cli, 'search ""')
    assert result.exit_code != 0

    mock_search.assert_not_called()


@mock.patch('vimwiki_cli.diary.index')
def test_diary_default(mock_index, runner):
    result = runner.invoke(cli, 'diary')
    assert result.exit_code == 0

    # index() should be invoked if no command is specified:
    mock_index.assert_called_with()


@mock.patch('vimwiki_cli.wiki.Wiki.diary_generate_links')
def test_diary_generate_links(mock_diary_generate_links, runner):
    result = runner.invoke(cli, 'diary generate-links')
    assert result.exit_code == 0

    mock_diary_generate_links.assert_called_with()


@mock.patch('vimwiki_cli.wiki.Wiki.diary_index')
def test_diary_index(mock_diary_index, runner):
    result = runner.invoke(cli, 'diary index')
    assert result.exit_code == 0

    mock_diary_index.assert_called_with()


@mock.patch('vimwiki_cli.wiki.Wiki.make_diary_note')
def test_diary_today(mock_make_diary_note, runner):
    result = runner.invoke(cli, 'diary today')
    assert result.exit_code == 0

    mock_make_diary_note.assert_called_with()


@mock.patch('vimwiki_cli.wiki.Wiki.make_tomorrow_diary_note')
def test_diary_tomorrow(mock_make_tomorrow_diary_note, runner):
    result = runner.invoke(cli, 'diary tomorrow')
    assert result.exit_code == 0

    mock_make_tomorrow_diary_note.assert_called_with()


@mock.patch('vimwiki_cli.wiki.Wiki.make_yesterday_diary_note')
def test_diary_yesterday(mock_make_yesterday_diary_note, runner):
    result = runner.invoke(cli, 'diary yesterday')
    assert result.exit_code == 0

    mock_make_yesterday_diary_note.assert_called_with()


@mock.patch('vimwiki_cli.wiki.Wiki.generate_tag_links')
@pytest.mark.parametrize('args,expected', [
    ('PAGE', ('PAGE', ())),
    ('PAGE TAG1 TAG2', ('PAGE', ('TAG1', 'TAG2')))
])
def test_tags_generate_links(mock_generate_tag_links, runner, args, expected):
    result = runner.invoke(cli, 'tags generate-links ' + args)
    assert result.exit_code == 0

    mock_generate_tag_links.assert_called_with(*expected)


@mock.patch('vimwiki_cli.wiki.Wiki.generate_tag_links')
def test_tags_generate_links_with_empty_page(mock_generate_tag_links, runner):
    result = runner.invoke(cli, 'tags generate-links ""')
    assert result.exit_code != 0

    mock_generate_tag_links.assert_not_called()


@mock.patch('vimwiki_cli.wiki.Wiki.rebuild_tags')
@pytest.mark.parametrize('args,expected', [
    ('', False),
    ('--all', True)
])
def test_tags_rebuild(mock_rebuild_tags, runner, args, expected):
    result = runner.invoke(cli, 'tags rebuild ' + args)
    assert result.exit_code == 0

    mock_rebuild_tags.assert_called_with(expected)


@mock.patch('vimwiki_cli.wiki.Wiki.search_tags')
def test_search_tags(mock_search_tags, runner):
    result = runner.invoke(cli, 'tags search PATTERN')
    assert result.exit_code == 0

    mock_search_tags.assert_called_with('PATTERN')


@mock.patch('vimwiki_cli.wiki.Wiki.search_tags')
def test_search_tags_with_empty_pattern(mock_search_tags, runner):
    result = runner.invoke(cli, 'tags search ""')
    assert result.exit_code != 0

    mock_search_tags.assert_not_called()
