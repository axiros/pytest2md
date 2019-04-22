# coding:utf-8
"""
"""

import pytest, json, os, time
import pytest2md as p2m  # this is our markdown tutorial generation tool

from functools import partial
from uuid import uuid4
import unittest
import time
import json
import sys
import uuid


p2m = p2m.P2M(__file__, fn_target_md='docs/Changelog.md')


# run = partial(p2m.bash_run, no_cmd_path=True)


class Test1(unittest.TestCase):
    def test_changelog(self):
        """

        # Changelog Management

        [p2m]<SRC>

        """
        p2m.bash_run('cat "/etc/hosts"')

        p2m.md_from_source_code()
        p2m.write_markdown(with_source_ref=True, make_toc=True)


if __name__ == '__main__':

    unittest.main()
