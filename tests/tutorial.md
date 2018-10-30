


This is a set of tools, generating parts of a markdown document while
testing it.

Example: This README.md was built from running this file in `pytest`:

```python
"""
Creates The Tutorial - while testing its functions.

"""

import subprocess as sp
import pytest
import os
import time
from ast import literal_eval as ev

import pytest_to_md as ptm

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

        Lets run a bash command (cat that file again) and assert on its results:
        Note that the command is shown in the readme, while its result can be
        asserted upon.

        """
            % __file__
        )

        ptm.md(t)

        res = ptm.bash_run('cat "%(fn_md)s"' % ptm.ctx, no_cmd_path=True)
        assert 'This README.md was built' in res[0]['res']

    def test_write(self):
        """has to be the last 'test'"""
        # default is ../README.md
        ptm.write_readme()
```

Lets run a bash command (cat that file again) and assert on its results:
Note that the command is shown in the readme, while its result can be
asserted upon.

```bash
$ cat "/Users/gk/GitHub/pytest_to_md/tests/tutorial.md"



This is a set of tools, generating parts of a markdown document while
testing it.

Example: This README.md was built from running this file in `pytest`:

```python
"""
Creates The Tutorial - while testing its functions.

"""

import subprocess as sp
import pytest
import os
import time
from ast import literal_eval as ev

import pytest_to_md as ptm

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

        Lets run a bash command (cat that file again) and assert on its results:
        Note that the command is shown in the readme, while its result can be
        asserted upon.

        """
            % __file__
        )

        ptm.md(t)

        res = ptm.bash_run('cat "%(fn_md)s"' % ptm.ctx, no_cmd_path=True)
        assert 'This README.md was built' in res[0]['res']

    def test_write(self):
        """has to be the last 'test'"""
        # default is ../README.md
        ptm.write_readme()
```

Lets run a bash command (cat that file again) and assert on its results:
Note that the command is shown in the readme, while its result can be
asserted upon.
```