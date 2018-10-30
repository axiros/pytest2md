#!/usr/bin/env bash

echo "Uploading to pip"
set -x
pytest tests || exit 1

clean () {
    rm -rf ./dist
    rm -rf ./pytest_to_md.egg-info
    rm -rf ./build
}
clean
python setup.py clean sdist bdist_wheel
twine upload ./dist/*
clean







