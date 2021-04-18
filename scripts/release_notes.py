#!/usr/bin/env python3
# Copyright (c) 2021 Steven Stallion
# All rights reserved.
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

import argparse
import logging
import sys
from pprint import pformat
from textwrap import indent

import keepachangelog

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="""
        Generate release notes from a changelog that conforms to Keep a
        Changelog v1.0.0 (https://keepachangelog.com/en/1.0.0/).
        """)

    parser.add_argument('-f', '--file', nargs='?', default='CHANGELOG.md',
                        help='read changes from file (default: CHANGELOG.md)')

    parser.add_argument('-o', '--output', nargs='?', default=sys.stdout,
                        type=argparse.FileType('w'),
                        help='write output to file (default: <stdout>)', metavar='FILE')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase output verbosity')

    parser.add_argument('version', help='version to generate')

    args = parser.parse_args()

    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=logging.DEBUG if args.verbose else logging.INFO)

    logger.debug('Reading changes from %s', args.file)
    changes = keepachangelog.to_raw_dict(args.file)

    logger.debug('Found changes:\n%s', indent(pformat(changes), '  '))
    if args.version not in changes:
        logger.error('Unable to find version %s', args.version)
        sys.exit(1)

    logger.debug('Writing output to %s', args.output.name)
    with args.output as f:
        input = changes[args.version]['raw']
        for index, line in enumerate(input.splitlines(True)):
            # keepachangelog will strip bare newlines, which can impact
            # readability. Newlines are added around headings to minimally
            # conform to the Google Markdown style guide.
            if line.startswith('#'):
                if index > 0:
                    f.write('\n')
                f.write('%s\n' % line)
            else:
                f.write(line)

    return 0


if __name__ == '__main__':
    sys.exit(main())
