


This is a set of tools, *generating* documentation, while verifying the documented
claims about code behaviour - without the need to adapt the source code, e.g. by modifying
doc strings.

Example: This "README.md" was mainly built from this file (while it was run as
a test within pytest):

```python
"""
Creates Readme - while testing functions of ptm.


While pytest is running we simply assemble from scratch an intermediate .md file
in append only mode, located within the tests folder.
This we insert between two seperators in the target markdown file, as the last
test function, done.
"""
import pytest_to_md as ptm
import pytest, json, os, time
from functools import partial


breakpoint = ptm.breakpoint

here, fn = ptm.setup(__file__)

run = partial(ptm.bash_run, no_cmd_path=True)


class TestChapter1:
    def test_one(self):
        t = (
            """

        This is a set of tools, *generating* documentation, while verifying the documented
        claims about code behaviour - without the need to adapt the source code, e.g. by modifying
        doc strings.

        Example: This "README.md" was mainly built from this file (while it was run as
        a test within pytest):

        <from_file: %s>

        """
            % __file__
        )

        ptm.md(t)
        ptm.md(
            """
        Lets run a bash command and assert on its results.
        Note that the command is shown in the readme, incl. result and the result
        can be asserted upon.
        """
        )

        res = run('cat "/etc/hosts" | grep localhost')
        assert '127.0.0.1' in res[0]['res']

    def test_two(self):
        res = run(['ls "%(fn_md)s"' % ptm.cfg, 'ls -lta /etc/hosts'])
        assert 'tutorial' in res[0]['res']
        assert 'hosts' in res[1]['res']

    def test_file_create_show(self):
        ptm.md(
            """When working with files, the `sh_file` function is helpful,
                producing output like this one:"""
        )
        ts = time.ctime()
        c = json.dumps({'a': [{'testfile': 'created'}, 'at', ts]}, indent=4)
        # if content is given it will create it:
        ptm.sh_file('/tmp/foo', lang='javascript', content=c)

        # check existance:
        with open('/tmp/foo') as fd:
            assert fd.read() == c

    def test_mdtool(self):
        md = """
        The module does offer also some link replacement feature,
        via the `mdtool` app (Help: See `mdtool -h`).  
        Example: [pytest_to_md]<SRC> was linked by replacing "SRC" with the path
        to a file matching, under a given directory, prefixed by an arbitrary base URL.

        - At normal runs of pytest, that base URL is just a local `file://` link,
        but before pushes one can set these e.g. to the github base URL or the repo.
        - `[key-values]` constructs are supported as well, example following:

        """
        ptm.md(md)

    def test_sh_code(self):
        ptm.md('Source code showing is done like this:')
        ptm.sh_code(self.test_sh_code)
        ptm.md(
            '> Is [title:this,fmatch:test_tutorial,lmatch:exotic]<SRC> an exotic form of a recursion? ;-)  '
        )

    def test_write(self):
        """has to be the last 'test'"""
        # default is ../README.md
        ptm.write_readme()
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
$ ls "/Users/gk/GitHub/pytest_to_md/tests/tutorial.md"
/Users/gk/GitHub/pytest_to_md/tests/tutorial.md

$ ls -lta /etc/hosts
-rw-r--r--  1 root  wheel  978 Aug 13 08:16 /etc/hosts
```
When working with files, the `sh_file` function is helpful,
                producing output like this one:
```javascript
$ cat "foo"
{
    "a": [
        {
            "testfile": "created"
        },
        "at",
        "Tue Nov 20 23:16:22 2018"
    ]
}
```

The module does offer also some link replacement feature,
via the `mdtool` app (Help: See `mdtool -h`).  
Example: [pytest_to_md]<SRC> was linked by replacing "SRC" with the path
to a file matching, under a given directory, prefixed by an arbitrary base URL.

- At normal runs of pytest, that base URL is just a local `file://` link,
but before pushes one can set these e.g. to the github base URL or the repo.
- `[key-values]` constructs are supported as well, example following:

Source code showing is done like this:
```python
    def test_sh_code(self):
        ptm.md('Source code showing is done like this:')
        ptm.sh_code(self.test_sh_code)
        ptm.md(
            '> Is [title:this,fmatch:test_tutorial,lmatch:exotic]<SRC> an exotic form of a recursion? ;-)  '
        )

```
> Is [title:this,fmatch:test_tutorial,lmatch:exotic]<SRC> an exotic form of a recursion? ;-)  