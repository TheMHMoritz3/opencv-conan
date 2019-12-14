#!/usr/bin/env bash

set -ex

if [[ "$(uname -s)" == 'Darwin' ]]; then
    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
    fi
    pyenv activate conan
fi

python build.py

conan upload opencv-conan/4.2.0-pre@themhmoritz3/BachelorThesisProjectDependencies  -r https://dl.bintray.com/themhmoritz3/BachelorThesisProjectDependencies --all
