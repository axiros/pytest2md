#!/usr/bin/env bash

echo "Uploading to pip"
set -x
here="$(unset CDPATH && cd "$(dirname "$BASH_SOURCE")" && echo $PWD)"
cd "$here"
export NOLINKREPL=true
pytest tests || exit 1
git commit -am 'pre_pypi_upload'
#slt="https://github.com/axiros/DevApps/blob/`git rev-parse  HEAD`"
#slt="$slt/%(file)s%(#Lline)s"
echo "Setting links..."
mdtool set_links src_link_tmpl="github" md_file="README.md"
exit
git push

clean () {
    rm -rf ./dist
    rm -rf ./pytest_to_md.egg-info
    rm -rf ./build
}
clean
python setup.py clean sdist bdist_wheel
twine upload ./dist/*
clean







