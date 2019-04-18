"""
How to upload

python setup.py clean sdist bdist_wheel
twine upload dist/*
"""


# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md')) as fd:
    md = fd.read()

P = find_packages('.')

setup(
    name='pytest2md',
    version='20190428',
    description='Create and run markdown Readmes from within pytest',
    long_description=md,
    long_description_content_type='text/markdown',
    # for parametrizing the command line:
    install_requires=[],
    packages=P,
    package_dir={'': '.'},
    include_package_data=True,
    url='https://github.com/axiros/pytest2md',
    author='gk',
    author_email='gk@axiros.com',
    license='BSD',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Markup',
        'Operating System :: POSIX',
        'License :: OSI Approved :: BSD License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    keywords=['markdown', 'markup', 'testing', 'pytest'],
    py_modules=['pytest2md', 'strutils'],
    # entry_points={'console_scripts': ['mdtool = mdtool:run']},
    zip_safe=False,
)
