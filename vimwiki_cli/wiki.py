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

import os

from .editor import Command, GlobalCommand, LocalCommand, DiaryCommand


class Wiki(object):
    DEFAULT_EDITOR = os.getenv('EDITOR', 'vim')
    DEFAULT_COUNT = None
    DEFAULT_SELECT = False
    DEFAULT_OPEN_MATCHES = False
    DEFAULT_OPEN_TABS = False

    def __init__(self, **options):
        self._options = options

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__,
                           self._options)

    @property
    def editor(self):
        return self._options.get('editor', Wiki.DEFAULT_EDITOR)

    @property
    def count(self):
        return self._options.get('count', Wiki.DEFAULT_COUNT)

    @property
    def select(self):
        return self._options.get('select', Wiki.DEFAULT_SELECT)

    @property
    def open_matches(self):
        return self._options.get('open_matches', Wiki.DEFAULT_OPEN_MATCHES)

    @property
    def open_tabs(self):
        return self._options.get('open_tabs', Wiki.DEFAULT_OPEN_TABS)

    # Help commands:

    def help(self):
        """Open plugin help file."""
        Command(self, 'help vimwiki.txt', 'only').run()

    # Global commands:

    def index(self):
        """Open wiki index."""
        GlobalCommand(self, 'VimwikiIndex').run()

    def diary_index(self):
        """Open diary index."""
        GlobalCommand(self, 'VimwikiDiaryIndex').run()

    def make_diary_note(self):
        """Open diary page for today."""
        GlobalCommand(self, 'VimwikiMakeDiaryNote').run()

    def make_yesterday_diary_note(self):
        """Open diary page for yesterday."""
        GlobalCommand(self, 'VimwikiMakeYesterdayDiaryNote').run()

    def make_tomorrow_diary_note(self):
        """Open diary page for tomorrow."""
        GlobalCommand(self, 'VimwikiMakeTomorrowDiaryNote').run()

    # Local commands:

    def goto(self, page):
        """Open or create page."""
        assert page.strip()
        LocalCommand(self, 'VimwikiGoto ' + page).run()

    def search(self, pattern):
        """Search wiki for text matching pattern."""
        assert pattern.strip()
        LocalCommand(self, 'silent! VimwikiSearch ' + pattern,
                     open_matches=True).run()

    def generate_links(self, page, pattern=''):
        """Create or update an overview of all pages in page."""
        assert page.strip()
        LocalCommand(self, 'VimwikiGoto ' + page, 'VimwikiGenerateLinks ' + pattern,
                     interactive=False, write_quit=True).run()

    def diary_generate_links(self):
        """Create or update an overview of diary pages."""
        DiaryCommand(self, 'VimwikiDiaryGenerateLinks',
                     interactive=False, write_quit=True).run()

    def all_html(self, all=False):
        """Convert all wiki pages to HTML."""
        LocalCommand(self, 'silent! VimwikiAll2HTML' + ('!' if all else ''),
                     interactive=False, quit=True).run()

    def check_links(self):
        """Search files and check reachability of links."""
        LocalCommand(self, 'VimwikiCheckLinks').run()

    def rebuild_tags(self, all=False):
        """Rebuild tag metadata."""
        LocalCommand(self, 'VimwikiRebuildTags' + ('!' if all else ''),
                     interactive=False, quit=True).run()

    def search_tags(self, pattern):
        """Search wiki for tags matching pattern."""
        assert pattern.strip()
        LocalCommand(self, 'silent! VimwikiSearchTags ' + pattern,
                     open_matches=True).run()

    def generate_tag_links(self, page, tags=()):
        """Create or update an overview of all tags in page."""
        assert page.strip()
        LocalCommand(self, 'VimwikiGoto ' + page, 'VimwikiGenerateTagLinks ' + ' '.join(tags),
                     interactive=False, write_quit=True).run()
