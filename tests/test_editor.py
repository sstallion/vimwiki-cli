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

import subprocess

import mock
import pytest

from vimwiki_cli.editor import *


@pytest.fixture(autouse=True)
def cmd_options():
    return {}


@pytest.fixture
def cmd(wiki, cmd_options):
    return Command(wiki, 'COMMAND', **cmd_options)


@pytest.fixture
def cmd_global(wiki, cmd_options):
    return GlobalCommand(wiki, 'GLOBAL_COMMAND', **cmd_options)


@pytest.fixture
def cmd_local(wiki, cmd_options):
    return LocalCommand(wiki, 'LOCAL_COMMAND', **cmd_options)


@pytest.fixture
def cmd_diary(wiki, cmd_options):
    return DiaryCommand(wiki, 'DIARY_COMMAND', **cmd_options)


@pytest.mark.parametrize('wiki_options', [{'open_matches': True}])
@pytest.mark.parametrize('cmd_options', [{'interactive': True, 'open_matches': True}])
def test_interactive_with_matches(cmd):
    assert cmd._args == ['COMMAND', 'lopen']


@pytest.mark.parametrize('wiki_options', [{'open_tabs': True}])
@pytest.mark.parametrize('cmd_options', [{'interactive': True}])
def test_interactive_with_tabs(cmd):
    assert cmd._args == ['$tabnew', 'COMMAND']


@pytest.mark.parametrize('cmd_options', [{'interactive': True, 'quit': True}])
def test_interactive_with_quit(cmd):
    assert cmd._args == ['COMMAND', 'q!']


@pytest.mark.parametrize('cmd_options', [{'interactive': True, 'write_quit': True}])
def test_interactive_with_write_quit(cmd):
    assert cmd._args == ['COMMAND', 'wq!']


@mock.patch('os.execvp')
@pytest.mark.parametrize('wiki_options', [{'editor': 'EDITOR'}])
@pytest.mark.parametrize('cmd_options', [{'interactive': True}])
def test_interactive_run(mock_execvp, cmd):
    cmd.run()

    mock_execvp.assert_called_with('EDITOR', ['EDITOR', '-c', 'COMMAND'])


@mock.patch('os.execvp', side_effect=OSError)
@pytest.mark.parametrize('wiki_options', [{'editor': 'EDITOR'}])
@pytest.mark.parametrize('cmd_options', [{'interactive': True}])
def test_interactive_run_with_error(mock_execvp, cmd):
    with pytest.raises(OSError):
        cmd.run()


@pytest.mark.parametrize('wiki_options', [{'open_matches': True}])
@pytest.mark.parametrize('cmd_options', [{'interactive': False, 'open_matches': True}])
def test_noninteractive_with_matches(cmd):
    assert 'lopen' not in cmd._args


@pytest.mark.parametrize('wiki_options', [{'open_tabs': True}])
@pytest.mark.parametrize('cmd_options', [{'interactive': False}])
def test_noninteractive_with_tabs(cmd):
    assert '$tabnew' not in cmd._args


@pytest.mark.parametrize('cmd_options', [{'interactive': False, 'quit': True}])
def test_noninteractive_with_quit(cmd):
    assert cmd._args == ['COMMAND', 'q!']


@pytest.mark.parametrize('cmd_options', [{'interactive': False, 'write_quit': True}])
def test_noninteractive_with_write_quit(cmd):
    assert cmd._args == ['COMMAND', 'wq!']


@mock.patch('sys.exit')
@mock.patch('subprocess.Popen')
@pytest.mark.parametrize('wiki_options', [{'editor': 'EDITOR'}])
@pytest.mark.parametrize('cmd_options', [{'interactive': False}])
def test_noninteractive_run(mock_Popen, mock_exit, cmd):
    mock_Popen.return_value.communicate.return_value = (b'', b'')
    mock_Popen.return_value.returncode = 0

    cmd.run()

    mock_Popen.assert_called_with(['EDITOR', '-c', 'COMMAND'],
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)

    mock_exit.assert_called_with(mock_Popen.return_value.returncode)


@mock.patch('subprocess.Popen', side_effect=OSError)
@pytest.mark.parametrize('wiki_options', [{'editor': 'EDITOR'}])
@pytest.mark.parametrize('cmd_options', [{'interactive': False}])
def test_noninteractive_run_with_error(mock_Popen, cmd):
    with pytest.raises(OSError):
        cmd.run()


@mock.patch('sys.exit')
@mock.patch('subprocess.Popen')
@pytest.mark.parametrize('wiki_options', [{'editor': 'EDITOR'}])
@pytest.mark.parametrize('cmd_options', [{'interactive': False}])
def test_noninteractive_run_with_returncode(mock_Popen, mock_exit, cmd):
    mock_Popen.return_value.communicate.return_value = (b'', b'')
    mock_Popen.return_value.returncode = ~0

    cmd.run()

    mock_exit.assert_called_with(mock_Popen.return_value.returncode)


def test_global_with_defaults(cmd_global):
    assert cmd_global._args == ['GLOBAL_COMMAND']


@pytest.mark.parametrize('wiki_options', [{'count': 42}])
def test_global_with_count(cmd_global):
    assert cmd_global._args == ['GLOBAL_COMMAND 42']


@pytest.mark.parametrize('wiki_options', [{'count': 42, 'select': True}])
def test_global_with_count_and_select(cmd_global):
    assert 'VimwikiUISelect' not in cmd_global._args


@pytest.mark.parametrize('wiki_options', [{'select': True}])
def test_global_select(cmd_global):
    assert cmd_global._args == ['VimwikiUISelect', 'GLOBAL_COMMAND']


@pytest.mark.parametrize('wiki_options', [{'select': True}])
@pytest.mark.parametrize('cmd_options', [{'interactive': False}])
def test_global_with_select_forces_interactive(cmd_global):
    assert cmd_global.interactive is True


def test_local_with_defaults(cmd_local):
    assert cmd_local._args == ['VimwikiIndex', 'LOCAL_COMMAND']


def test_diary_with_defaults(cmd_diary):
    assert cmd_diary._args == ['VimwikiDiaryIndex', 'DIARY_COMMAND']
