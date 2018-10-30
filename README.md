# pytest_to_md: Tools to generate README.md while testing their claims.

[blacksvg]: https://img.shields.io/badge/code%20style-black-000000.svg
[black]: https://github.com/ambv/black

<!-- badges: http://thomas-cokelaer.info/blog/2014/08/1013/ -->

<!-- autogen tutorial -->


This is a set of tools, generating parts of a markdown document while
testing it.

Example: This README.md was built from running this file in `pytest`:

```python
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

    def test_two(self):
        res = ptm.bash_run(
            ['ls -lta %(fn_md)s' % ptm.cfg, 'ls /etc/hosts'], no_cmd_path=True
        )
        assert 'tutorial' in res[0]['res']
        assert 'hosts' in res[1]['res']

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
$ ls -lta /Users/gk/GitHub/pytest_to_md/tests/tutorial.md
-rw-r--r--  1 gk  staff  1810 Oct 30 18:43 /Users/gk/GitHub/pytest_to_md/tests/tutorial.md

$ ls /etc/hosts
/etc/hosts
```
<!-- autogen tutorial -->
