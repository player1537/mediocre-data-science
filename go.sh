#!/usr/bin/env bash
# vim :set ts=4 sw=4 sts=4 et:
die() { printf $'Error: %s\n' "$*" >&2; exit 1; }
root=$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)
self=${BASH_SOURCE[0]:?}
project=${root##*/}
pexec() { >&2 printf exec; >&2 printf ' %q' "$@"; >&2 printf '\n'; exec "$@"; }
prun() { >&2 printf run; >&2 printf ' %q' "$@"; >&2 printf '\n'; "$@"; }
go() { "go-$@"; }
next() { "${FUNCNAME[1]:?}-$@"; }
#---

data=${root:?}/data
temp=${root:?}/temp

environment=${temp:?}/venv

go-New-Environment() {
    prun uv venv --seed \
        "${environment:?}" \
    ##

    pexec ln -sf \
        "${environment:?}" \
    ##
}

go-Initialize-Environment() {
    pexec "${environment:?}/bin/pip" install \
        -e "${root:?}/[dev,test]" \
    ##
}

go-Invoke-Notebook() {
    local path
    path=${1:?need path to notebook}

    if ! [ -f "${path:?}" ]; then
        die "Notebook not found: ${path:?}"
    fi

    local dest
    dest=${temp:?}/${path##*/}
    dest=${dest%.*}.ipynb

    pexec "${environment:?}/bin/jupytext" \
        --from py:percent \
        --opt comment_magics=false \
        --to notebook \
        --execute \
        --update \
        --set-kernel python3 \
        --run-path "${root:?}" \
        --output "${dest:?}" \
        "${path:?}" \
    ##
}

go-Invoke-Tests() {
    pexec "${environment:?}/bin/pytest" \
        "${root:?}/tests" \
        "$@" \
    ##
}

#---
test -f "${root:?}/env.sh" && source "${_:?}"
"go-$@"
