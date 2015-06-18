#!/usr/bin/env bash
# @see: http://blog.sensible.io/2014/05/09/supercharge-your-vim-into-ide-with-ctags.html
cd "`pwd`"
ctags -R --languages=ruby --exclude=.git --exclude=log .
