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
import sys

import click

from . import __version__
from .context import *
from .diary import diary
from .tags import tags

logger = logging.getLogger(__name__)


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True,
             epilog='Report issues to https://github.com/sstallion/vimwiki-cli/issues.')
@click.option('--editor',
              help='Editor to launch, defaults to $EDITOR or vim.')
@click.option('--count', type=int,
              help='Index of wiki to open.')
@click.option('--select', is_flag=True,
              help='Select wiki from interactive list.')
@click.option('--open-matches', is_flag=True,
              help='Open search results by default.')
@click.option('--open-tabs', is_flag=True,
              help='Open pages in a new tab by default.')
@click.option('-v', '--verbose', is_flag=True,
              help='Increase output verbosity.')
@click.version_option(message='%(prog)s %(version)s')
@click.pass_context
def cli(ctx, *args, **kwargs):
    """Vimwiki Command-Line Interface

    vimwiki-cli is a command-line interface to Vimwiki, a plugin for the Vim
    text editor.  It provides a front-end for interactive editor commands and
    can be used to automate repetitive tasks such as rebuilding tag metadata
    and generating links, all from the command line.

    Global options may also be configured using environment variables:

    \b
    VIMWIKI_EDITOR        See --editor.
    VIMWIKI_COUNT         See --count.
    VIMWIKI_SELECT        See --select.
    VIMWIKI_OPEN_MATCHES  See --open-matches.
    VIMWIKI_OPEN_TABS     See --open-tabs.

    If no command is specified, the wiki index will be opened by default.
    """
    verbose = kwargs.pop('verbose', False)
    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=logging.DEBUG if verbose else logging.INFO)

    logger.debug('Python %s', sys.version)
    logger.debug('Version %s', __version__)

    make_wiki(ctx, *args, **kwargs)
    if ctx.invoked_subcommand is None:
        ctx.invoke(index)


@cli.command()
@click.option('--all', is_flag=True,
              help='Rebuild all files, not just those that are newer.')
@pass_wiki
def all_html(wiki, all):
    """Convert all wiki pages to HTML."""
    wiki.all_html(all)


@cli.command()
@pass_wiki
def check_links(wiki):
    """Search files and check reachability of links."""
    wiki.check_links()


@cli.command()
@click.argument('page', callback=validate_nonempty)
@click.argument('pattern', required=False, default='')
@pass_wiki
def generate_links(wiki, page, pattern):
    """Create or update an overview of all pages in PAGE.

    An optional PATTERN may be specified to indicate which files to search for
    using a glob path.
    """
    wiki.generate_links(page, pattern)


@cli.command()
@click.argument('page', callback=validate_nonempty)
@pass_wiki
def goto(wiki, page):
    """Open or create PAGE."""
    wiki.goto(page)


@cli.command()
@pass_wiki
def help(wiki):
    """Open plugin help file."""
    wiki.help()


@cli.command(hidden=True)
@pass_wiki
def index(wiki):
    """Open wiki index."""
    wiki.index()


@cli.command()
@click.argument('pattern', callback=validate_nonempty)
@pass_wiki
def search(wiki, pattern):
    """Search wiki for text matching PATTERN."""
    wiki.search(pattern)


cli.add_command(diary)
cli.add_command(tags)

if __name__ == '__main__':  # pragma: no cover
    cli()
