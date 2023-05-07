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

from vimwiki_cli.wiki import *


@mock.patch('vimwiki_cli.wiki.Command')
def test_help(mock_cmd, wiki):
    wiki.help()

    mock_cmd.assert_called_with(wiki, 'help vimwiki.txt', 'only')


@mock.patch('vimwiki_cli.wiki.GlobalCommand')
def test_index(mock_cmd, wiki):
    wiki.index()

    mock_cmd.assert_called_with(wiki, 'VimwikiIndex')


@mock.patch('vimwiki_cli.wiki.GlobalCommand')
def test_diary_index(mock_cmd, wiki):
    wiki.diary_index()

    mock_cmd.assert_called_with(wiki, 'VimwikiDiaryIndex')


@mock.patch('vimwiki_cli.wiki.GlobalCommand')
def test_make_diary_note(mock_cmd, wiki):
    wiki.make_diary_note()

    mock_cmd.assert_called_with(wiki, 'VimwikiMakeDiaryNote')


@mock.patch('vimwiki_cli.wiki.GlobalCommand')
def test_make_yesterday_diary_note(mock_cmd, wiki):
    wiki.make_yesterday_diary_note()

    mock_cmd.assert_called_with(wiki, 'VimwikiMakeYesterdayDiaryNote')


@mock.patch('vimwiki_cli.wiki.GlobalCommand')
def test_make_tomorrow_diary_note(mock_cmd, wiki):
    wiki.make_tomorrow_diary_note()

    mock_cmd.assert_called_with(wiki, 'VimwikiMakeTomorrowDiaryNote')


@mock.patch('vimwiki_cli.wiki.LocalCommand')
def test_goto(mock_cmd, wiki):
    wiki.goto('PAGE')

    mock_cmd.assert_called_with(wiki, 'VimwikiGoto PAGE')


@mock.patch('vimwiki_cli.wiki.LocalCommand')
def test_search(mock_cmd, wiki):
    wiki.search('PATTERN')

    mock_cmd.assert_called_with(wiki, 'silent! VimwikiSearch PATTERN',
                                open_matches=True)


@mock.patch('vimwiki_cli.wiki.LocalCommand')
@pytest.mark.parametrize('args,expected', [
    (('PAGE',), ('VimwikiGoto PAGE', 'VimwikiGenerateLinks ')),
    (('PAGE', 'PATTERN'), ('VimwikiGoto PAGE', 'VimwikiGenerateLinks PATTERN'))
])
def test_generate_links(mock_cmd, wiki, args, expected):
    wiki.generate_links(*args)

    mock_cmd.assert_called_with(wiki, *expected,
                                interactive=False, write_quit=True)


@mock.patch('vimwiki_cli.wiki.DiaryCommand')
def test_diary_generate_links(mock_cmd, wiki):
    wiki.diary_generate_links()

    mock_cmd.assert_called_with(wiki, 'VimwikiDiaryGenerateLinks',
                                interactive=False, write_quit=True)


@mock.patch('vimwiki_cli.wiki.LocalCommand')
@pytest.mark.parametrize('args,expected', [
    (False, 'silent! VimwikiAll2HTML'),
    (True, 'silent! VimwikiAll2HTML!')
])
def test_all_html(mock_cmd, wiki, args, expected):
    wiki.all_html(args)

    mock_cmd.assert_called_with(wiki, expected,
                                interactive=False, quit=True)


@mock.patch('vimwiki_cli.wiki.LocalCommand')
def test_check_links(mock_cmd, wiki):
    wiki.check_links()

    mock_cmd.assert_called_with(wiki, 'VimwikiCheckLinks')


@mock.patch('vimwiki_cli.wiki.LocalCommand')
@pytest.mark.parametrize('args,expected', [
    (False, 'VimwikiRebuildTags'),
    (True, 'VimwikiRebuildTags!')
])
def test_rebuild_tags(mock_cmd, wiki, args, expected):
    wiki.rebuild_tags(args)

    mock_cmd.assert_called_with(wiki, expected,
                                interactive=False, quit=True)


@mock.patch('vimwiki_cli.wiki.LocalCommand')
def test_search_tags(mock_cmd, wiki):
    wiki.search_tags('PATTERN')

    mock_cmd.assert_called_with(wiki, 'silent! VimwikiSearchTags PATTERN',
                                open_matches=True)


@mock.patch('vimwiki_cli.wiki.LocalCommand')
@pytest.mark.parametrize('args,expected', [
    (('PAGE',), ('VimwikiGoto PAGE', 'VimwikiGenerateTagLinks ')),
    (('PAGE', ('TAG1', 'TAG2')), ('VimwikiGoto PAGE', 'VimwikiGenerateTagLinks TAG1 TAG2'))
])
def test_generate_tag_links(mock_cmd, wiki, args, expected):
    wiki.generate_tag_links(*args)

    mock_cmd.assert_called_with(wiki, *expected,
                                interactive=False, write_quit=True)
