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


@click.group()
def tags():
    """Command group for interacting with tags."""


@tags.command()
@click.argument('page', callback=validate_nonempty)
@click.argument('tags', nargs=-1)
@pass_wiki
def generate_links(wiki, page, tags):
    """Create or update an overview of all tags in PAGE.

    An optional list of TAGS may be specified to restrict output.  This
    command requires tag metadata built using the rebuild subcommand.
    """
    wiki.generate_tag_links(page, tags)


@tags.command()
@click.option('--all', is_flag=True,
              help='Rebuild all files, not just those that are newer.')
@pass_wiki
def rebuild(wiki, all):
    """Rebuild tag metadata."""
    wiki.rebuild_tags(all)


@tags.command()
@click.argument('pattern', callback=validate_nonempty)
@pass_wiki
def search(wiki, pattern):
    """Search wiki for tags matching PATTERN."""
    wiki.search_tags(pattern)
