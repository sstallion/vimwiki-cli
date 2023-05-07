#!/usr/bin/env bash
#
# A pre-commit hook script to execute non-interactive vimwiki commands to
# rebuild tag metadata and generate links before commit.
#
# This hook relies on the following configuration options:
#
# vimwiki.options -- Extra options to pass to the vimwiki command
# vimwiki.linkspage -- Page which contains generated links
# vimwiki.taglinkspage -- Page which contains generated tag links
# vimwiki.generatelinks -- Generate links before commit (bool)
# vimwiki.generatediarylinks -- Generate diary links before commit (bool)
# vimwiki.generatetaglinks -- Generate tag links before commit (bool)
# vimwiki.rebuildtags -- Rebuild tag metadata before commit (bool)
#
# To enable this hook, copy or link this file to ".git/hooks/pre-commit".

if git config --get-colorbool color.interactive
then
	# See https://github.com/vimwiki/vimwiki/blob/master/doc/logo.svg
	say_prefix='\e[90mvim\e[92m|\e[37mwiki\e[0m'
else
	say_prefix='vimwiki'
fi

say () {
	printf '%b: %s' "$say_prefix" "$*"
}

say_done () {
	printf 'done.\n'
}

# Exit if no changes staged for commit
if git diff --cached --diff-filter=tuxb --quiet
then
	exit 0
fi

# Stash untracked changes
git stash push --keep-index --include-untracked --quiet >/dev/null 2>&1

trap 'git stash pop --quiet >/dev/null 2>&1' 0
trap 'exit 1' 1 2 3 15

options=$(git config vimwiki.options)

if test "$(git config --bool vimwiki.generatelinks || echo false)" = true
then
	page=$(git config vimwiki.linkspage || echo index)

	say 'Generating links...'
	vimwiki $options generate-links "$page" || exit
	say_done
fi

if test "$(git config --bool vimwiki.generatediarylinks || echo false)" = true
then
	say 'Generating diary links...'
	vimwiki $options diary generate-links || exit
	say_done
fi

if test "$(git config --bool vimwiki.rebuildtags || echo false)" = true
then
	say 'Rebuilding tag metadata...'
	vimwiki $options tags rebuild || exit
	say_done
fi

if test "$(git config --bool vimwiki.allhtml || echo false)" = true
then
	say 'Converting all wiki pages to HTML...'
	vimwiki $options all-html || exit
	say_done
fi

if test "$(git config --bool vimwiki.generatetaglinks || echo false)" = true
then
	page=$(git config vimwiki.taglinkspage || echo index)

	say 'Generating tag links...'
	vimwiki $options tags generate-links "$page" || exit
	say_done
fi

# Add changes to index
git add --all
