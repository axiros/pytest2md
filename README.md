# Small tools to generate markdown - while testing contained claims.

[![Build Status](https://travis-ci.org/axiros/pytest2md.svg?branch=master)](https://travis-ci.org/axiros/pytest2md) [![codecov](https://codecov.io/gh/axiros/pytest2md/branch/master/graph/badge.svg)](https://codecov.io/gh/axiros/pytest2md)[![PyPI    version][pypisvg]][pypi] [![][blacksvg]][black]

[blacksvg]: https://img.shields.io/badge/code%20style-black-000000.svg
[black]: https://github.com/ambv/black
[pypisvg]: https://img.shields.io/pypi/v/pytest2md.svg
[pypi]: https://badge.fury.io/py/pytest2md

<!-- badges: http://thomas-cokelaer.info/blog/2014/08/1013/ -->


<!-- only hoster for this repo is github, so we fix the links: -->
<!-- md_links_for: github -->

- [Inline Python Function Execution](#inline-python-function-execution)
- [Tools](#tools)
- [Files](#files)
- [Link Replacements](#link-replacements)
    - [Code Repo Hoster Specific Source Links](#code-repo-hoster-specific-source-links)
        - [Setting a link template](#setting-a-link-template)
        - [Link Refs](#link-refs)
    - [Summary](#summary)
- [Isolation](#isolation)


Few things are more annoying than stuff which does not work as announced,
especially when you find out only after an invest of time and energy.

Documentation is often prone to produce such situations, since hard to keep
100% in sync with the code evolution.

<!-- autogen tutorial -->


This is a set of tools, *generating* documentation, while verifying the documented
claims about code behaviour - without the need to adapt the source code, e.g. by modifying
doc strings.

Example: This "README.md" was built into [this](./README.tmpl.md) template,
where [html comment style placeholders][README.tmpl.md]
had been replaced while running pytest on this testfile:

```python
"""
Creates Readme - while testing functions of p2m.


While pytest is running we simply assemble from scratch an intermediate .md file
in append only mode, located within the tests folder.
This we insert between two seperators in the target markdown file, as the last
test function, done.
"""
import pytest2md as p2m
import pytest, json, os, time
from functools import partial
from uuid import uuid4
import json

# py2.7 compat:
breakpoint = p2m.breakpoint

here, fn = p2m.setup(__file__, fn_target_md='../README.md')

# parametrizing the shell run results:
run = partial(p2m.bash_run, no_cmd_path=True)


class TestChapter1:
    def test_one(self):
        t = """

        This is a set of tools, *generating* documentation, while verifying the documented
        claims about code behaviour - without the need to adapt the source code, e.g. by modifying
        doc strings.

        Example: This "README.md" was built into [this](./README.tmpl.md) template,
        where [title:html comment style placeholders,fmatch:README.tmpl.md,show_raw:True]<SRC>
        had been replaced while running pytest on this testfile:

        <from_file: %s>

        """ % (
            __file__,
        )

        p2m.md(t)
        p2m.md(
            """
        Lets run a bash command and assert on its results.
        Note that the command is shown in the readme, incl. result and the result
        can be asserted upon.
        """
        )

        res = run('cat "/etc/hosts" | grep localhost')
        assert '127.0.0.1' in res[0]['res']

    def test_two(self):
        res = run(['ls "%(fn_md)s"' % p2m.cfg, 'ls -lta /etc/hosts'])
        assert 'tutorial' in res[0]['res']
        assert 'hosts' in res[1]['res']

    def test_simple_pyfuncs(self):
        """
        # Inline Python Function Execution

        via the `md_from_source_code` function you can write fluent markdown
        (tested) python combos:
        """

        def foo():
            hi = 'hello world'
            assert 'world' in hi
            print(hi.replace('world', 'joe'))

        """
        The functions are evaluated and documented in the order they show up
        within the textblocks.

        > Please keep tripple apostrophes - we split the text blocks,
        searching for those.

        State is kept within the outer pytest function, like normally in python.
        I.e. if you require new state, then start a new pytest function.

        Stdout is redirected to an output collector function, i.e. if you print
        this does result in an "Output" block. If the printout starts with
        "MARKDOWN:" then we won't wrap that output into fenced code blocks but
        display as is.

        > If the string 'breakpoint' occurs in a function body, we won't redirect
        standardout for displaying output.

        # Tools

        Also there are few tools available, e.g this one:

        """

        def mdtable():
            from pytest2md import html_table as ht

            t = ht(
                [['joe', 'doe'], ['suzie', 'wong']],
                ['first', 'last'],
                summary='names. click to open...',
            )
            assert 'details' in t
            assert 'joe</td' in t
            print(t)

        """
        Another tool is the simple TOC generator, invoked like at the end of this file.
        """

        p2m.md_from_source_code()

    def test_file_create_show(self):
        p2m.md(
            """
        # Files
        When working with files, the `sh_file` function is helpful,
        producing output like this one:"""
        )
        ts = time.ctime()
        c = json.dumps({'a': [{'testfile': 'created'}, 'at', ts]}, indent=4)
        # if content is given it will create it:
        fn = '/tmp/' + str(uuid4())
        p2m.sh_file(fn, lang='javascript', content=c)

        # check existance:
        with open(fn) as fd:
            assert fd.read() == c
        os.unlink(fn)

    def test_mdtool(self):
        md = """
        # Link Replacements

        Technical markdown content wants to link to source code often.
        How to get those links working and that convenient?

        The module does offer also some source finding / link replacement feature,
        via the [mdtool]<SRC> module. The latter link was built simply by this:

        ```
        [mdtool]<SRC>
        ```

        Other example: This [pytest2md]<SRC> link was created by replacing "SRC" with the path
        to a file matching, under a given directory, prefixed by an arbitrary base URL.

        ## Code Repo Hoster Specific Source Links

        Github, Gitlab, Bitbucked or Plain directory based static content servers
        all have their conventional URLs regarding those links.

        Since all of these are just serving static content w/o js possibilities,
        you have to parametrize the intended hoster in your environment, before
        running a pytest / push cycle. That way the links will be working on the hoster.

        Currently we understand the following namespaces for links:


        ```javascript
        _link_names_
        ```

        ### Setting a link template

        - `export MD_LINKS_FOR=github   ` # before running pytest / push
        - `<!-- md_links_for: github -->` # in the markdown template, static

        The latter can be overwritten by environ, should you want to push from time to time
        to a different code hoster.

        ### Link Refs

        We minimize the problem of varying generated target markdown, dependent on the hoster.
        How? Like [any problem in IT is solved](https://en.wikipedia.org/wiki/Fundamental_theorem_of_software_engineering).


        By building [reference links](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#links)
        the differences of e.g. a README.md for github vs. gitlab is
        restricted to the links section on the end of the generated markdown.
        In the markdown bodies you'll just see link names, which remain the same.

        > Check the end of the [title:rendering result,fmatch:README.md,show_raw:True]<SRC> at the end of this README.md,
        in order to see the results for the hoster you are reading this markdown file currently.

        ## Summary

        - At normal runs of pytest, the link base URL is just a local `file://` link,

        - Before pushes one can set via environ (e.g. `export
          MD_LINKS_FOR=github`)  these e.g. to the github base URL or the repo.

        - `[key-values]` constructs are supported as well, extending to beyond
          just the base url. Example following:

        """.replace(
            '_link_names_',
            json.dumps(p2m.mdtool.known_src_links, indent=4, sort_keys=2),
        )
        p2m.md(md)

    def test_sh_code(self):
        p2m.md('Source code showing is done like this:')
        p2m.sh_code(self.test_sh_code)
        p2m.md(
            '> Is [title:this,fmatch:test_tutorial,lmatch:exotic]<SRC> an exotic form of a recursion? ;-)  '
        )

    def test_write(self):
        """has to be the last 'test'"""
        # default is ../README.md
        p2m.write_readme(with_source_ref=True, make_toc=True)
```


Lets run a bash command and assert on its results.
Note that the command is shown in the readme, incl. result and the result
can be asserted upon.
```bash
$ cat "/etc/hosts" | grep localhost
# localhost is used to configure the loopback interface
127.0.0.1  localhost lo sd1 sd3 sa1 sa2 sb1 sb2
::1             localhost
```
```bash
$ ls "/Users/gk/GitHub/pytest2md/tests/tutorial.md"
/Users/gk/GitHub/pytest2md/tests/tutorial.md

$ ls -lta /etc/hosts
-rw-r--r--  1 root  wheel  1047 Mar  1 11:35 /etc/hosts
```
# Inline Python Function Execution

via the `md_from_source_code` function you can write fluent markdown
(tested) python combos:
```python

hi = 'hello world'
assert 'world' in hi
print(hi.replace('world', 'joe'))
```
Output:
```
hello joe

```
The functions are evaluated and documented in the order they show up
within the textblocks.

> Please keep tripple apostrophes - we split the text blocks,
searching for those.

State is kept within the outer pytest function, like normally in python.
I.e. if you require new state, then start a new pytest function.

Stdout is redirected to an output collector function, i.e. if you print
this does result in an "Output" block. If the printout starts with
"MARKDOWN:" then we won't wrap that output into fenced code blocks but
display as is.

> If the string 'breakpoint' occurs in a function body, we won't redirect
standardout for displaying output.

# Tools

Also there are few tools available, e.g this one:

```python

from pytest2md import html_table as ht

t = ht(
    [['joe', 'doe'], ['suzie', 'wong']],
    ['first', 'last'],
    summary='names. click to open...',
)
assert 'details' in t
assert 'joe</td' in t
print(t)
```


<details>
        <summary>names. click to open...</summary>
        <table>
<tr><td>first</td><td>last</td></tr>
<tr><td>joe</td><td>doe</td></tr>
<tr><td>suzie</td><td>wong</td></tr>
</table>
        </details>
        


# Files
When working with files, the `sh_file` function is helpful,
producing output like this one:
```javascript
$ cat "0deedcae-662a-4380-8611-17c12464ea3e"
{
    "a": [
        {
            "testfile": "created"
        },
        "at",
        "Thu Apr 18 20:52:09 2019"
    ]
}
```

# Link Replacements

Technical markdown content wants to link to source code often.
How to get those links working and that convenient?

The module does offer also some source finding / link replacement feature,
via the [mdtool module. The latter link was built simply by this:

```
[mdtool]<SRC>
```

Other example: This [pytest2md link was created by replacing "SRC" with the path
to a file matching, under a given directory, prefixed by an arbitrary base URL.

## Code Repo Hoster Specific Source Links

Github, Gitlab, Bitbucked or Plain directory based static content servers
all have their conventional URLs regarding those links.

Since all of these are just serving static content w/o js possibilities,
you have to parametrize the intended hoster in your environment, before
running a pytest / push cycle. That way the links will be working on the hoster.

Currently we understand the following namespaces for links:


```javascript
{
    "github": "https://github.com/%(gh_repo_name)s/blob/%(git_rev)s/%(path)s%(line:#L%s)s",
    "github_raw": "https://raw.githubusercontent.com/%(gh_repo_name)s/%(git_rev)s/%(path)s%(line:#L%s)s",
    "static": "file://%(src_base_dir)s/%(path)s",
    "static_raw": "file://%(src_base_dir)s/%(path)s"
}
```

### Setting a link template

- `export MD_LINKS_FOR=github   ` # before running pytest / push
- `<!-- md_links_for: github -->` # in the markdown template, static

The latter can be overwritten by environ, should you want to push from time to time
to a different code hoster.

### Link Refs

We minimize the problem of varying generated target markdown, dependent on the hoster.
How? Like [any problem in IT is solved](https://en.wikipedia.org/wiki/Fundamental_theorem_of_software_engineering).


By building [reference links](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#links)
the differences of e.g. a README.md for github vs. gitlab is
restricted to the links section on the end of the generated markdown.
In the markdown bodies you'll just see link names, which remain the same.

> Check the end of the [rendering result][README.md] at the end of this README.md,
in order to see the results for the hoster you are reading this markdown file currently.

## Summary

- At normal runs of pytest, the link base URL is just a local `file://` link,

- Before pushes one can set via environ (e.g. `export
  MD_LINKS_FOR=github`)  these e.g. to the github base URL or the repo.

- `[key-values]` constructs are supported as well, extending to beyond
  just the base url. Example following:

Source code showing is done like this:
```python
    def test_sh_code(self):
        p2m.md('Source code showing is done like this:')
        p2m.sh_code(self.test_sh_code)
        p2m.md(
            '> Is [title:this,fmatch:test_tutorial,lmatch:exotic]<SRC> an exotic form of a recursion? ;-)  '
        )

```
> Is [this][test_tutorial.py] an exotic form of a recursion? ;-)  

*Auto generated by [pytest2md](https://github.com/axiros/pytest2md), running [test_tutorial.py][test_tutorial.py]*

<!-- autogen tutorial -->

# Isolation

None. If you would screw up your host running pytest normally, then you will
get the same result, when running markdown generating tests.


[Here](https://github.com/axiros/pycond) is a bigger tutorial,
[created][dasrc] from `pytest2md`. There you'll learn in addition to shell
runners how to generate markdown from running inline python functions...

[dasrc]: https://github.com/axiros/DevApps/blob/master/tests/test_tutorial.py


<!-- autogenlinks -->
[README.md]: https://raw.githubusercontent.com/axiros/pytest2md/c1b4d5f4deb9da222739cfaaa4db27cb6a231707/README.md
[README.tmpl.md]: https://raw.githubusercontent.com/axiros/pytest2md/c1b4d5f4deb9da222739cfaaa4db27cb6a231707/README.tmpl.md
[test_tutorial.py]: https://github.com/axiros/pytest2md/blob/c1b4d5f4deb9da222739cfaaa4db27cb6a231707/tests/test_tutorial.py