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

import logging
import os
import subprocess
import sys

logger = logging.getLogger(__name__)


class Command(object):
    DEFAULT_INTERACTIVE = True
    DEFAULT_OPEN_MATCHES = False
    DEFAULT_QUIT = False
    DEFAULT_WRITE_QUIT = False

    def __init__(self, wiki, *args, **options):
        self._wiki = wiki
        self._options = options

        args = list(args)
        if self.interactive:
            if wiki.open_tabs:
                args.insert(0, '$tabnew')

            if self.open_matches and wiki.open_matches:
                args.append('lopen')

        if self.quit or self.write_quit:
            args.append('%sq!' % ('w' if self.write_quit else ''))

        self._args = args

    def __repr__(self):
        return '%s(%r, %r, %r)' % (self.__class__.__name__,
                                   self._wiki,
                                   self._args,
                                   self._options)

    @property
    def interactive(self):
        return self._options.get('interactive', Command.DEFAULT_INTERACTIVE)

    @property
    def open_matches(self):
        return self._options.get('open_matches', Command.DEFAULT_OPEN_MATCHES)

    @property
    def quit(self):
        return self._options.get('quit', Command.DEFAULT_QUIT)

    @property
    def write_quit(self):
        return self._options.get('write_quit', Command.DEFAULT_WRITE_QUIT)

    def run(self):
        """Run command in the editor.  This method does not return as
        interactive commands replace the runing process with the editor and
        non-interactive commands exit with the resulting return code.
        """
        logger.debug('Running %r' % self)

        args = [self._wiki.editor]
        for arg in self._args:
            args.extend(['-c', arg.strip()])

        logger.debug('Launching %r' % args)
        if self.interactive:
            os.execvp(args[0], args)
        else:
            process = subprocess.Popen(args,
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)

            (_, stderr) = process.communicate()
            if process.returncode != 0:
                logger.error(stderr.decode(sys.stderr.encoding))

            sys.exit(process.returncode)


class GlobalCommand(Command):

    def __init__(self, wiki, *args, **options):
        assert len(args) > 0

        args = list(args)
        if wiki.count is not None:
            args.insert(0, '%s %d' % (args.pop(0), wiki.count))

        elif wiki.select:
            args.insert(0, 'VimwikiUISelect')

            # Force interactive if VimwikiUISelect will be executed:
            options['interactive'] = True

        Command.__init__(self, wiki, *args, **options)


class LocalCommand(GlobalCommand):

    def __init__(self, wiki, *args, **options):
        GlobalCommand.__init__(self, wiki, 'VimwikiIndex', *args, **options)


class DiaryCommand(GlobalCommand):

    def __init__(self, wiki, *args, **options):
        GlobalCommand.__init__(self, wiki, 'VimwikiDiaryIndex', *args, **options)
