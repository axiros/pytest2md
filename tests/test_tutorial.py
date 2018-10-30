"""
Creates Readme - while testing functions of ptm.


While pytest is running we simply assemble from scratch an intermediate .md file
in append only mode, located within the tests folder.
This we insert between two seperators in the target markdown file, as the last
test function, done.
"""
import pytest_to_md as ptm

import pytest
from functools import partial


breakpoint = ptm.breakpoint

here, fn = ptm.setup(__file__)

run = partial(ptm.bash_run, no_cmd_path=True)


class TestChapter1:
    def test_one(self):
        t = (
            """

        This is a set of tools, generating parts of a markdown document while
        testing it.

        Example: This README.md was built from this file (while it was run as
        a test within pytest):

        <from-file: %s>

        [Here](https://github.com/axiros/DevApps) is a bigger tutorial created
        from `pytest_to_md` ([src](https://github.com/axiros/DevApps/tests/test_tutorial.py)).

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

    def test_write(self):
        """has to be the last 'test'"""
        # default is ../README.md
        ptm.write_readme()
