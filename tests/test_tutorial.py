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
from uuid import uuid4

# py2.7 compat:
breakpoint = ptm.breakpoint

here, fn = ptm.setup(__file__, fn_target_md='../README.md')

# parametrizing the shell run results:
run = partial(ptm.bash_run, no_cmd_path=True)


class TestChapter1:
    def test_one(self):
        t = """

        This is a set of tools, *generating* documentation, while verifying the documented
        claims about code behaviour - without the need to adapt the source code, e.g. by modifying
        doc strings.

        Example: This "README.md" was built into [this](./README.tmpl.md) template,
        where the [title:placeholder,fmatch:README.tmpl.md,lmatch:autogen]<SRC>
        content was replaced while running pytest on this testfile:

        <from_file: %s>

        """ % (
            __file__,
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
        fn = '/tmp/' + str(uuid4())
        ptm.sh_file(fn, lang='javascript', content=c)

        # check existance:
        with open(fn) as fd:
            assert fd.read() == c
        os.unlink(fn)

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
