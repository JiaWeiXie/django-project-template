#!/usr/bin/env bash
echo "Copy this script to yuor shell(.bash_profile/.zshrc)."
echo "=============================="
echo 'if command -v pyenv 1>/dev/null 2>&1; then\n  export PIPENV_VENV_IN_PROJECT=true\n  export PIPENV_DONT_LOAD_ENV=1\n  eval "$(pipenv --completion)" \nfi'

#if command -v pyenv 1>/dev/null 2>&1; then
#  export PIPENV_VENV_IN_PROJECT=true
#  export PIPENV_DONT_LOAD_ENV=1
#  eval "$(pipenv --completion)"
#fi