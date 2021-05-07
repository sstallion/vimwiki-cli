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

import click

from .context import *


@click.group(invoke_without_command=True)
@click.pass_context
def diary(ctx):
    """Command group for interacting with the diary.

    If no command is specified, the diary index will be opened by default.
    """
    if ctx.invoked_subcommand is None:
        ctx.invoke(index)


@diary.command()
@pass_wiki
def generate_links(wiki):
    """Create or update an overview of diary pages."""
    wiki.diary_generate_links()


@diary.command(hidden=True)
@pass_wiki
def index(wiki):
    """Open diary index."""
    wiki.diary_index()


@diary.command()
@pass_wiki
def today(wiki):
    """Open diary page for today."""
    wiki.make_diary_note()


@diary.command()
@pass_wiki
def tomorrow(wiki):
    """Open diary page for tomorrow."""
    wiki.make_tomorrow_diary_note()


@diary.command()
@pass_wiki
def yesterday(wiki):
    """Open diary page for yesterday."""
    wiki.make_yesterday_diary_note()
