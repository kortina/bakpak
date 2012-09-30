#!/bin/bash
### determine if the currently checked out local branch is behind origin/master
git fetch origin \
&& git rev-list --left-right `git branch -a | grep "^\*" | cut -c 3-`...origin/master -- 2>/dev/null >/tmp/git_upstream_status_delta \
&& RIGHT_AHEAD=$(grep -c '^>' /tmp/git_upstream_status_delta) \
&& [ "$RIGHT_AHEAD" -ne "0" ] \
&& echo "Your branch is $RIGHT_AHEAD commits behind origin/master"
&& exit 2

### First, fetch all the origin branch info
### Then, compute the delta's between the current branch and origin master
### Count the number of diffs where the origin/master is ahead
### Echo a warning if your local branch is behind,
### and if so, exit
