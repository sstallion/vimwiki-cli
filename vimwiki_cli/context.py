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

from .wiki import Wiki

CONTEXT_SETTINGS = {
    'auto_envvar_prefix': 'VIMWIKI',
    'default_map': {
        'editor': Wiki.DEFAULT_EDITOR,
        'count': Wiki.DEFAULT_COUNT,
        'select': Wiki.DEFAULT_SELECT,
        'open_matches': Wiki.DEFAULT_OPEN_MATCHES,
        'open_tabs': Wiki.DEFAULT_OPEN_TABS
    }
}

pass_wiki = click.make_pass_decorator(Wiki, ensure=True)


def make_wiki(ctx, *args, **kwargs):
    """Create Wiki instance as user data and add to context."""
    ctx.obj = Wiki(**kwargs)


def validate_nonempty(ctx, param, value):
    """Validate parameter is not an empty string."""
    if not value.strip():
        raise click.BadParameter('value cannot be empty')

    return value
