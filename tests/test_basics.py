# coding:utf-8
"""
"""
import os
import unittest
import pytest, json, os, time
import pytest2md as p2mm  # this is our markdown tutorial generation tool
from pytest2md import mdtool
from functools import partial

here = os.path.abspath(os.path.dirname(__file__))
test_mod = os.path.basename(__file__).split('.py', 1)[0]


class TestGenerateMarkdown(unittest.TestCase):
    """We fix the output 100% with this test """

    def setUp(self):
        os.unlink('/tmp/foo.md') if os.path.exists('/tmp/foo.md') else 0
        self.p2m = p2mm.P2M(__file__, fn_target_md='/tmp/foo.md')
        self.run = partial(self.p2m.bash_run, no_cmd_path=True)

    def test_init(self):
        os.system('mkdir -p /tmp/root/docs/templates')
        os.system('touch /tmp/root/docs/templates/foo.md')

        p2mt = p2mm.P2M(__file__, fn_target_md='/tmp/root/docs/foo.md')
        assert p2mt.ctx == {
            'd_assets': here + '/assets',
            'd_test': here,
            'fn_target_md': '/tmp/root/docs/foo.md',
            'fn_target_md_tmpl': '/tmp/root/docs/templates/foo.md',
            'fn_test_file': __file__,
            'md_sep': '<!-- autogen tutorial -->',
            'md': [],
            'name': 'basics',
        }

    def test_from_src_code(self):
        'hi'
        """
        Hello
        """
        i = 42

        def f1():
            print(i)

        self.p2m.md_from_source_code()
        md = self.p2m.ctx['md']
        l = [
            '\nhi  \nHello  \n\n```python\nprint(i)\n```\nOutput:\n\n```\n42\n```'
        ]
        assert l == md

    def test_from_src_code2(self):
        """
        Hello
        """
        i = 42

        def f1():
            print(i)

        self.p2m.md_from_source_code()
        md = self.p2m.ctx['md']
        l = ['\nHello  \n\n```python\nprint(i)\n```\nOutput:\n\n```\n42\n```']
        assert l == md

    def test_from_src_code2(self):
        i = 42

        def f1():
            print(i)

        'foo'
        self.p2m.md_from_source_code()
        md = self.p2m.ctx['md']
        l = ['\n\n```python\nprint(i)\n```\nOutput:\n\n```\n42\n```\n\nfoo  ']
        assert l == md

    def test_from_src_code3(self):
        'foo'
        self.p2m.md_from_source_code()
        md = self.p2m.ctx['md']
        l = ['\nfoo  ']
        assert l == md

    def test_from_src_code4(self):
        def f1():
            print(42)

        self.p2m.md_from_source_code()
        md = self.p2m.ctx['md']
        l = ['\n```python\nprint(42)\n```\nOutput:\n\n```\n42\n```']
        assert l == md

    def test_from_src_code_printing_markdown(self):
        def f1():
            print("""MARKDOWN: # h1\ninner""")

        self.p2m.md_from_source_code()
        md = self.p2m.ctx['md']
        # the test func gets that "MARKDOWN:" output ususally from a helper
        # func, i.e. user doe not see it, e.g. print(to_html(res))
        l = [
            '\n```python\nprint("""MARKDOWN: # h1\\ninner""")\n```\n # h1\ninner\n'
        ]
        assert l == md

    def test_tool_as_json(self):
        'foo'

        def f1(p2m=self.p2m):  # no needed in real life, p2m on module level
            print(p2m.as_json({'a': {'b': {'c': 1}}}))

        self.p2m.md_from_source_code()
        md = self.p2m.ctx['md']
        # the test func gets that "MARKDOWN:" output ususally from a helper
        # func, i.e. user doe not see it, e.g. print(to_html(res))
        l = [
            '\n'
            'foo  \n'
            '\n'
            '```python\n'
            "print(p2m.as_json({'a': {'b': {'c': 1}}}))\n"
            '```\n'
            '\n'
            '```javascript\n'
            '{\n'
            '    "a": {\n'
            '        "b": {\n'
            '            "c": 1\n'
            '        }\n'
            '    }\n'
            '}\n'
            '```\n'
        ]
        assert l == md

    def test_tool_html_table(self):
        'foo'

        def f1(p2m=self.p2m):  # no needed in real life, p2m on module level
            print(p2m.html_table([['foo', 'bar'], [42, 42]], ('name', 'val')))

        """
        as details:
        """

        def f1(p2m=self.p2m):  # no needed in real life, p2m on module level
            print(
                p2m.html_table(
                    [['foo', 'bar'], [42, 42]],
                    ('name', 'val'),
                    summary='click...',
                )
            )

        self.p2m.md_from_source_code()
        md = self.p2m.ctx['md']
        l = [
            '\n'
            'foo  \n'
            '\n'
            '```python\n'
            'print(\n'
            '    p2m.html_table(\n'
            "        [['foo', 'bar'], [42, 42]],\n"
            "        ('name', 'val'),\n"
            "        summary='click...',\n"
            '    )\n'
            ')\n'
            '```\n'
            '\n'
            '<details>\n'
            '        <summary>click...</summary>\n'
            '        <table>\n'
            '<tr><td>name</td><td>val</td></tr>\n'
            '<tr><td>foo</td><td>bar</td></tr>\n'
            '<tr><td>42</td><td>42</td></tr>\n'
            '</table>\n'
            '        </details>\n'
            '        \n'
            '\n'
            '\n'
            'as details:  \n'
            '\n'
            '```python\n'
            'print(\n'
            '    p2m.html_table(\n'
            "        [['foo', 'bar'], [42, 42]],\n"
            "        ('name', 'val'),\n"
            "        summary='click...',\n"
            '    )\n'
            ')\n'
            '```\n'
            '\n'
            '<details>\n'
            '        <summary>click...</summary>\n'
            '        <table>\n'
            '<tr><td>name</td><td>val</td></tr>\n'
            '<tr><td>foo</td><td>bar</td></tr>\n'
            '<tr><td>42</td><td>42</td></tr>\n'
            '</table>\n'
            '        </details>\n'
            '        \n'
        ]
        assert l == md

    def test_tool_convert_to_staticmethods(self):
        'A Py2 tool'

        def f1(p2m=self.p2m):  # no needed in real life, p2m on module level
            class A:
                def foo(b):
                    print(b)

            p2m.convert_to_staticmethods(A)
            A.foo(42)

        self.p2m.md_from_source_code()
        md = self.p2m.ctx['md']
        l = [
            '\n'
            'A Py2 tool  \n'
            '\n'
            '```python\n'
            'class A:\n'
            '    def foo(b):\n'
            '        print(b)\n'
            '\n'
            'p2m.convert_to_staticmethods(A)\n'
            'A.foo(42)\n'
            '```\n'
            'Output:\n'
            '\n'
            '```\n'
            '42\n'
            '```\n'
        ]
        assert l == md

    def test_bashrun(self):
        r = self.run('cat /etc/hosts')
        assert len(r) == 1
        assert r[0]['cmd'] == 'cat /etc/hosts'
        assert r[0]['res']
        assert [i for i in r[0].keys()] in (['cmd', 'res'], ['res', 'cmd'])
        md = self.p2m.ctx['md'][0]
        assert md.startswith('```bash\n')
        assert 'cat /etc' in md.splitlines()[1]
        assert md.splitlines()[-1] == '```'

    def test_sh_file(self):
        r = self.p2m.sh_file(__file__)
        for r in (r, self.p2m.ctx['md'][0]):
            assert r.startswith('```python')
            assert 'test_sh_file' in r

    def test_sh_code(self):
        def f():
            print('42')

        r = self.p2m.sh_code(f)
        l = ["```python\n        def f():\n            print('42')\n\n```"]
        assert l == self.p2m.ctx['md']


class TestWriteMarkdown(unittest.TestCase):
    def setUp(self):
        os.unlink('/tmp/foo.md') if os.path.exists('/tmp/foo.md') else 0
        self.p2m = p2mm.P2M(__file__, fn_target_md='/tmp/foo.md')
        self.run = partial(self.p2m.bash_run, no_cmd_path=True)

    def test_write_md_1(self):
        self.p2m.ctx['md'] = ['# h1', 'hi']
        md = self.p2m.write_markdown(
            no_write=True, make_toc=False, no_link_repl=False
        )
        l = '\n<!-- autogen tutorial -->\n# h1\nhi\n<!-- autogen tutorial -->\n'
        assert l == md

    def test_write_md_2(self):
        self.p2m.ctx['md'] = ['# h1', 'hi']
        md = self.p2m.write_markdown(no_write=True, make_toc=False)
        l = '\n<!-- autogen tutorial -->\n# h1\nhi\n<!-- autogen tutorial -->\n'
        assert l == md

    def test_link_simple(self):
        self.p2m.ctx['md'] = ['# h1', 'hi[%s]<SRC> [nix]' % test_mod]
        md = self.p2m.write_markdown(no_write=True, make_toc=False)
        lm = """
<!-- autogen tutorial -->
# h1
hi[%s][%s.py] [nix]
<!-- autogen tutorial -->


<!-- autogenlinks -->
[%s.py]: file://
        """ % (
            test_mod,
            test_mod,
            test_mod,
        )
        assert lm.strip() == md.strip().rsplit('file://', 1)[0] + 'file://'
        e = os.environ
        e['MD_LINKS_FOR'] = 'name:github,gh_repo_name:A/B,git_rev:1234'
        this = here.rsplit('/', 1)[1] + '/%s.py' % test_mod
        md = self.p2m.write_markdown(no_write=True, make_toc=False)
        l = """
<!-- autogen tutorial -->
# h1
hi[%s][%s.py] [nix]
<!-- autogen tutorial -->


<!-- autogenlinks -->
[%s.py]: https://github.com/A/B/blob/1234/%s
""" % (
            test_mod,
            test_mod,
            test_mod,
            this,
        )
        assert md.strip() == l.strip()
        os.environ['MD_LINKS_FOR'] = ''

    def test_link_match_only(self):
        foo = '1555854118.9871481555854118.9871481555854118.987148'
        self.p2m.ctx['md'] = [
            'check [fmatch:%s,lmatch:%s]<SRC> that' % (test_mod, foo)
        ]
        e = os.environ
        e['MD_LINKS_FOR'] = 'name:github,gh_repo_name:A/B,git_rev:1234'
        md = self.p2m.write_markdown(no_write=True, make_toc=False)
        # the line number at the end:
        nr = md.rsplit('#L', 1)[1].strip()
        this = here.rsplit('/', 1)[1] + '/%s.py' % test_mod
        l = """
        <!-- autogen tutorial -->
check [test_basics][test_basics.py#%s] that
<!-- autogen tutorial -->


<!-- autogenlinks -->
[test_basics.py#%s]: https://github.com/A/B/blob/1234/%s#L%s
""" % (
            (nr, nr, this, nr)
        )
        assert l.strip() == md.strip()
        os.environ['MD_LINKS_FOR'] = ''


class TestLinks(unittest.TestCase):
    def setUp(self):
        self.mdt = partial(
            mdtool.MDTool,
            tests_dir=here,
            src_link_tmpl_name='name:github,gh_repo_name:A/B,git_rev:1234',
        )

    def test_sq_bracket_links(self):
        m = self.mdt('[title:foo,fmatch:%s]' % test_mod)
        r = m.do_set_links()
        assert r[0] == '[title:foo,fmatch:test_basics]'
        m = self.mdt('[title:foo,fmatch:%s]<SRC>' % test_mod)
        r = m.do_set_links()
        l = """
        [foo][test_basics.py]

<!-- autogenlinks -->
[test_basics.py]: https://github.com/A/B/blob/1234/tests/test_basics.py
        """
        assert r[0].strip() == l.strip()

    def test_curly_bracket_links(self):
        return 0
        # later
        uniq = 'asklajndfiansidfuansdfi'
        m = self.mdt('[title:foo,fmatch:%s]' % test_mod)
        r = m.do_set_links()
        assert r[0] == '[title:foo,fmatch:test_basics]'
        m = self.mdt('[title:foo,fmatch:%s]<SRC>' % test_mod)


def pl(l):
    """debug helper"""
    print('\n'.join(l))


if __name__ == '__main__':

    unittest.main()
