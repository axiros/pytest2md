---

author: gk
version: 190915

---

# Generating Markdown - While Testing Contained Claims

[![Build Status](https://travis-ci.org/axiros/pytest2md.svg?branch=master)](https://travis-ci.org/axiros/pytest2md) [![codecov](https://codecov.io/gh/axiros/pytest2md/branch/master/graph/badge.svg)](https://codecov.io/gh/axiros/pytest2md)[![PyPI    version][pypisvg]][pypi] [![][blacksvg]][black]

[blacksvg]: https://img.shields.io/badge/code%20style-black-000000.svg
[black]: https://github.com/ambv/black
[pypisvg]: https://img.shields.io/pypi/v/pytest2md.svg
[pypi]: https://badge.fury.io/py/pytest2md

<!-- badges: http://thomas-cokelaer.info/blog/2014/08/1013/ -->


<!-- only hoster for this repo is github, so we fix the links: -->
<!-- md_links_for: github -->

<!-- TOC -->

# Table Of Contents

- <a name="toc1"></a>[Inline Python Function Execution](#inline-python-function-execution)
- <a name="toc2"></a>[Features](#features)
    - <a name="toc3"></a>[html_table](#html-table)
    - <a name="toc4"></a>[sh_file](#sh-file)
    - <a name="toc5"></a>[bash_run](#bash-run)
    - <a name="toc6"></a>[md_from_source_code](#md-from-source-code)
    - <a name="toc7"></a>[Table of Contents](#table-of-contents)
- <a name="toc8"></a>[Link Replacements](#link-replacements)
    - <a name="toc9"></a>[Spec](#spec)
    - <a name="toc10"></a>[Code Repo Hoster Specific Source Links](#code-repo-hoster-specific-source-links)
        - <a name="toc11"></a>[Setting a link template](#setting-a-link-template)
        - <a name="toc12"></a>[Link Refs](#link-refs)
    - <a name="toc13"></a>[Summary](#summary)
- <a name="toc14"></a>[Tips](#tips)
- <a name="toc15"></a>[Isolation](#isolation)

<!-- TOC -->

Few things are more annoying than stuff which does not work as announced,
especially when you find out only after an invest of time and energy.

Documentation is often prone to produce such situations, since hard to keep
100% in sync with the code evolution.

<!-- autogen tutorial -->


This is a set of tools, *generating* documentation, while verifying the documented
claims about code behaviour - without the need to adapt the source code, e.g. by modifying
doc strings:

![](./assets/shot1.png)

> When the documentation is using a lot of code examples then a very welcome
additional benefit of writing it like shown is the availability of [source
code autoformatters](https://github.com/ambv/black).

Other Example:

This "README.md" was built into [this](./.README.tmpl.md) template,
where [html comment style placeholders][.README.tmpl.md]
had been replaced while running pytest on [test_tutorial](./tests/test_tutorial.py).



Lets run a bash command and assert on its results.
Note that the command is shown in the readme, incl. result and the result
can be asserted upon.

```bash
$ cat "/etc/hosts" | grep localhost
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
```

```bash
$ ls "/home/gk/repos/pytest2md/tests"
assets
__pycache__
test_basics.py
test_changelog.py
test_tutorial.py

$ ls -lta /etc/hosts
-rw-r--r--. 1 root root 286 Jul 22 12:08 /etc/hosts
```


----
Generated by:

# <a href="#toc1">Inline Python Function Execution</a>

via the `md_from_source_code` function you can write fluent markdown
(tested) python combos:  


```python
hi = 'hello world'
assert 'world' in hi
print(hi.replace('world', 'joe'))
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

# <a href="#toc2">Features</a>

## <a href="#toc3">html_table</a>
  


```python
ht = p2m.html_table

print(ht([['foo', 'bar'], ['bar', 'baz']], ['h1', 'h2']))
print('As details when summary arg is given:')
t = ht(
    [['joe', 'doe'], ['suzie', 'wong']],
    ['first', 'last'],
    summary='names. click to open...',
)
assert 'details' in t
assert 'joe</td' in t
print(t)
```
## <a href="#toc4">sh_file</a>

```javascript
$ cat "test_file.json"
{
    "a": [
        {
            "testfile": "created"
        },
        "at",
        "Sun Sep 22 18:32:13 2019"
    ]
}
```

<details><summary>as details</summary>


```javascript
$ cat "test_file.json"
{
    "a": [
        {
            "testfile": "created"
        },
        "at",
        "Sun Sep 22 18:32:13 2019"
    ]
}
```
</details>

[test_file.json](./tests/assets/sh_files/test_file.json)

[as link](./tests/assets/sh_files/test_file.json)


----
Generated by:



```python
# if content is given it will create it:
p2m.sh_file(fn, lang='javascript', content=c)
# summary arg creates a details structure:
p2m.sh_file(fn, lang='javascript', content=c, summary='as details')
# creates a link (say True to have the filename as link text)
p2m.sh_file(fn, lang='javascript', content=c, as_link=True)
p2m.sh_file(fn, lang='javascript', content=c, as_link='as link')
```
## <a href="#toc5">bash_run</a>

```bash
$ ./some_non_existing_command_in_assets arg1
/bin/sh: /home/gk/repos/pytest2md/tests/assets/some_non_existing_command_in_assets: No such file or directory
```

```bash
$ ls -lta | grep total | head -n 1
total 80
```

```bash
$ ls -lta
total 80
drwxr-xr-x.  8 gk armynyus  4096 Sep 22 18:32 .git
-rw-r--r--.  1 gk gk       14721 Sep 22 18:30 README.md
drwxr-xr-x.  8 gk armynyus  4096 Sep 22 18:25 .
drwxr-xr-x.  4 gk gk        4096 Sep 22 18:25 tests

...(output truncated - see link below)
```
- [Output](./tests/assets/bash_run_outputs/bash_run.txt) of `ls -lta`  


```bash
$ ls -lta
```

[ls -lta](./tests/assets/bash_run_outputs/bash_run.html)



----
Generated by:



```python
run = partial(p2m.bash_run, cmd_path_from_env=True)
# by default we search in normal environ for the command to run
# but we provide a switch to search in test assets.
# errors are redirected to stdout
res = p2m.bash_run(
    'some_non_existing_command_in_assets arg1',
    cmd_path_from_env=False,
    ign_err=True,
)
assert res[0]['exitcode'] != 0
res = run('ls -lta | grep total | head -n 1')
assert 'total' in res[0]['res']
res = run('ls -lta', into_file='bash_run.txt')
assert 'total' in res[0]['res']
# Ending with .html it converts ansi escape colors to html:
# simple link is created.
# (requires pip install ansi2html)
run('ls -lta', into_file='bash_run.html')
```
## <a href="#toc6">md_from_source_code</a>
Inserted markdown from running python.

Strings in double apos. are rendered, no need to call a render function.  


```python
md('Inserted markdown from running python.')
print('From output of running python ')
```
Output:

```
From output of running python
```

> More  markdown  


```python
print('From another function')
```
Output:

```
From another function
```

Strings can also contain instructions, like this (looked up in p2m.MdInline namespace class)


```bash
$ cd /etc; ls -lta | head -n 5
total 2240
drwxr-xr-x. 156 root root     12288 Sep 22 10:56 .
-rw-r--r--.   1 root root        67 Sep 22 10:56 resolv.conf
drwxr-xr-x.   5 root root      4096 Sep 19 19:23 systemd
-rw-r--r--.   1 root root    124464 Sep 19 19:00 ld.so.cache
```

Default inline functions (add your own in module headers):  


```python
print(
    [
        k
        for k in dir(pytest2md.MdInline)
        if not k.startswith('_')
    ]
)
```
Output:

```
['bash', 'sh_file']
```
----
Generated by
```python
        def some_test_function():
            """
            Strings in double apos. are rendered, no need to call a render function.
            """

            def func1():
                md('Inserted markdown from running python.')
                print('From output of running python ')

            """
            > More  markdown
            """

            def func2():
                print('From another function')

            """
            Strings can also contain instructions, like this (looked up in p2m.MdInline namespace class)

            <bash: cd MY_REPL_DIR; ls -lta | head -n 5>

            Default inline functions (add your own in module headers):
            """

            def known():
                print(
                    [
                        k
                        for k in dir(pytest2md.MdInline)
                        if not k.startswith('_')
                    ]
                )

            # repl dict simply replaces keys with values before any processing:
            p2m.md_from_source_code(repl={'MY_REPL_DIR': '/etc'})

```

## <a href="#toc7">Table of Contents</a>

    p2m.write_markdown(with_source_ref=True, make_toc=True)

See this tutorial.


# <a href="#toc8">Link Replacements</a>

Technical markdown content wants to link to source code often.
How to get those links working and that convenient?

The module does offer also some source finding / link replacement feature,
via the [mdtool][mdtool.py] module. The latter link was built simply by this:

```
[mdtool]<SRC>
```


Other example: This [test_tutorial.py][test_tutorial.py] link was created by replacing "SRC" with the path
to a file matching, under a given directory, prefixed by an arbitrary base URL.

## <a href="#toc9">Spec</a>

These will be replaced:

`[title:this,fmatch:test_tutorial,lmatch:line_match] <SRC>` (remove space between] and <)

- title: The link title - text the user reads
- fmatch: substring match for the link destination file
- lmatch: Find matching line within that file
- show_raw: Link to raw version of file, not the one rendered by the
  repo server
- path: Fix file path (usually derived by fmach)
- line: Fix the line number of the link (usually done via lmatch)

## <a href="#toc10">Code Repo Hoster Specific Source Links</a>

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
    "static": "file://%(d_repo_base)s/%(path)s",
    "static_raw": "file://%(d_repo_base)s/%(path)s"
}
```

### <a href="#toc11">Setting a link template</a>

- `export MD_LINKS_FOR=github   ` # before running pytest / push
- `<!-- md_links_for: github -->` # in the markdown template, static

The latter can be overwritten by environ, should you want to push from time to time
to a different code hoster.

### <a href="#toc12">Link Refs</a>

We minimize the problem of varying generated target markdown, dependent on the hoster.
How? Like [any problem in IT is solved](https://en.wikipedia.org/wiki/Fundamental_theorem_of_software_engineering).


By building [reference links](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#links)
the differences of e.g. a README.md for github vs. gitlab is
restricted to the links section on the end of the generated markdown.
In the markdown bodies you'll just see link names, which remain the same.

> Check the end of the [rendering result][README.md] at the end of this README.md,
in order to see the results for the hoster you are reading this markdown file currently.

## <a href="#toc13">Summary</a>

- At normal runs of pytest, the link base URL is just a local `file://` link,

- Before pushes one can set via environ (e.g. `export
  MD_LINKS_FOR=github`)  these e.g. to the github base URL or the repo.

- `[key-values]` constructs are supported as well, extending to beyond
  just the base url. Example following:

Source code showing is done like this:

```python
    def test_sh_code(self):
        md('Source code showing is done like this:')
        p2m.sh_code(self.test_sh_code)
        md(
            '> Is [title:this,fmatch:test_tutorial,lmatch:exotic]<SRC> an exotic form of a recursion? ;-)  '
        )

```
> Is [this][test_tutorial.py#325] an exotic form of a recursion? ;-)  



<details><summary>Command Summary</summary>


```bash
cat "/etc/hosts" | grep localhost
ls "/home/gk/repos/pytest2md/tests"
ls -lta /etc/hosts
/home/gk/repos/pytest2md/tests/assets/some_non_existing_command_in_assets arg1
ls -lta | grep total | head -n 1
ls -lta
ls -lta
```
</details>




*Auto generated by [pytest2md](https://github.com/axiros/pytest2md), running [./tests/test_tutorial.py](./tests/test_tutorial.py)

<!-- autogen tutorial -->

# <a href="#toc14">Tips</a>

- Local Renderer:

    pip install grip

to get a local github compliant markdown renderer, reloading after changes of the generated markdown.

- Using fixtures with unittest style test classes

Create a `conftest.py` like:

```python
root@localhost tests]# cat conftest.py
import pytest
import pytest2md as p2m


@pytest.fixture(scope='class')
def write_md(request):
    def fin():
        request.cls.p2m.write_markdown(with_source_ref=True, make_toc=False)

    request.addfinalizer(fin)

```

then use like:

```
@pytest.mark.usefixtures('write_md')
class TestDevUsage(unittest.TestCase):
    p2m = p2m # on module level: p2m.P2M(__file__, fn_target_md='README.md')

    (...)

```




# <a href="#toc15">Isolation</a>

None. If you would screw up your host running pytest normally, then you will
get the same result, when running markdown generating tests.

----

[Here](https://github.com/axiros/pycond) is a bigger tutorial, from `pytest2md`.





<!-- autogenlinks -->
[.README.tmpl.md]: https://raw.githubusercontent.com/axiros/pytest2md/10cb20096909e6996618ae2da5ae3766abf6a766/.README.tmpl.md
[README.md]: https://raw.githubusercontent.com/axiros/pytest2md/10cb20096909e6996618ae2da5ae3766abf6a766/README.md
[mdtool.py]: https://github.com/axiros/pytest2md/blob/10cb20096909e6996618ae2da5ae3766abf6a766/pytest2md/mdtool.py
[test_tutorial.py]: https://github.com/axiros/pytest2md/blob/10cb20096909e6996618ae2da5ae3766abf6a766/tests/test_tutorial.py
[test_tutorial.py#325]: https://github.com/axiros/pytest2md/blob/10cb20096909e6996618ae2da5ae3766abf6a766/tests/test_tutorial.py#L325