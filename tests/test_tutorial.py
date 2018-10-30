"""
Creates Readme - while testing functions of ptm

"""
import pytest_to_md as ptm

import subprocess as sp
import pytest
import os
import time
from ast import literal_eval as ev


breakpoint = ptm.breakpoint

here, fn = ptm.setup(__file__)


class TestChapter1:
    def test_one(self):
        t = (
            """

        This is a set of tools, generating parts of a markdown document while
        testing it.

        Example: This README.md was built from running this file in `pytest`:

        <from-file: %s>

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

        res = ptm.bash_run(
            'cat "/etc/hosts" | grep localhost', no_cmd_path=True
        )
        assert '127.0.0.1' in res[0]['res']

    def test_write(self):
        """has to be the last 'test'"""
        # default is ../README.md
        ptm.write_readme()
