"""
Creates The Tutorial - while testing its functions.

"""

import subprocess as sp
import pytest
import os
import time
import pdb
import appdirs
from ast import literal_eval as ev

breakpoint = pdb.set_trace

# setup creates ctx like this:
# {'fn_md': '/Users/gk/GitHub/pytest_to_md/tests/tutorial.md',
#  'fn_readme': '/Users/gk/GitHub/pytest_to_md/README.md',
#  'here': '/Users/gk/GitHub/pytest_to_md/tests',
#  'md_sep': '<!-- autogen tutorial -->'}
ctx = {}

dflt_md_sep = '<!-- autogen tutorial -->'

DIR = lambda d: os.path.abspath(os.path.dirname(d))


def rpl(what, *with_):
    for w in with_:
        if not isinstance(w, (tuple, list)):
            w = (w, '')
        what = what.replace(w[0], w[1])
    return what


def setup(fn_test_file, fn_readme=None, md_sep=dflt_md_sep):
    """called at module level by pytest test module, which creates the md
    e.g. fn_test_file=/Users/gk/GitHub/pytest_to_md/tests/test_tutorial.py
    """

    ctx['md_sep'] = md_sep
    fnt = fn_test_file
    here = ctx['here'] = DIR(fnt)
    if not fn_readme:
        fn = ctx['fn_readme'] = DIR(here) + '/README.md'

    if not os.path.exists(fn):
        print('Creating', fn)
        with open(fn, 'w') as fd:
            fd.write('\n'.join(('', md_sep, 'will be autogened.', md_sep, '')))

    name = ctx['name'] = rpl(fn_test_file.rsplit('/', 1)[-1], 'test_', '.py')
    ctx['d_assets'] = here + '/' + name + '/'
    fn_md = ctx['fn_md'] = here + '/' + name + '.md'

    if os.path.exists(fn_md):
        os.unlink(fn_md)
    with open(fn_md, 'w') as fd:
        fd.write('')

    return here, fn_md


def write_readme():
    """
    addd the new version of the rendered tutorial into the main readme
    """
    fn = ctx['fn_md']
    with open(fn) as fd:
        tut = fd.read()

    fnr = ctx['fn_readme']
    with open(fnr) as fd:
        readm = fd.read()
    m = ctx['md_sep']
    pre, _, post = readm.split(m)
    with open(fnr, 'w') as fd:
        fd.write(''.join((pre, m, tut, '\n', m, post)))


code = """```code
%s
```"""
# fmt: off
nothing  = lambda s: s
python   = lambda s: code.replace('code', 'python')  % s
bash     = lambda s: code.replace('code', 'bash')  %s
markdown = lambda s: code.replace('code', 'markdown') % (s.replace('```', "``"))
# fmt: on


def md(paras, into=nothing):
    """writes markdown"""
    paras = [paras]
    lctx = {}
    lctx['in_code_block'] = False

    def deindent(p):
        pp = p.replace('\n', '')
        ind = len(pp) - len(pp.lstrip())
        if not ind:
            return p
        return '\n'.join(
            [l[ind:] if not l[:ind].strip() else l for l in p.splitlines()]
        )

    paras = [deindent(p) for p in paras]

    def repl(l, lctx=lctx):
        if '```' in l:
            lctx['in_code_block'] = not lctx['in_code_block']

        ff = '<from-file: '
        if l.strip().startswith(ff):
            pre, post = l.split(ff, 1)
            fn, post = post.rsplit('>', 1)
            if not fn.startswith('/'):
                fn = ctx['d_assets'] + fn
            if not os.path.exists(fn):
                s = l
            else:
                with open(fn) as fd:
                    s = fd.read().strip()
                if fn.endswith('.py'):
                    s = python(s)
                else:
                    s = code % s
            l = pre + s + post
        return l

    r = '\n'.join([repl(l) for para in paras for l in para.splitlines()])
    r = into(r)
    fn = ctx['fn_md']
    with open(fn, 'a') as fd:
        fd.write('\n' + r)


def bash_run(cmd, res_as=None, no_cmd_path=False, no_show_in_cmd=''):
    """runs unix commands, then writes results into the markdown"""
    if isinstance(cmd, str):
        cmds = [{'cmd': cmd, 'res': ''}]
    elif isinstance(cmd, list):
        cmds = [{'cmd': c, 'res': ''} for c in cmd]
    else:
        cmds = cmd
    orig_cmd = cmds[0]['cmd']
    if not res_as and orig_cmd.startswith('python -c'):
        res_as = python
    D = ctx['d_assets']

    for c in cmds:
        cmd = c['cmd']
        fncmd = cmd if no_cmd_path else (D + cmd)
        # run it:
        res = c['res'] = sp.getoutput(fncmd)
        if no_show_in_cmd:
            fncmd = fncmd.replace(no_show_in_cmd, '')
        # .// -> when there is no_cmd_path we would get that, ugly:
        # this is just for md output, not part of testing:
        c['cmd'] = fncmd.replace(D, './').strip().replace('.//', './')

    r = '\n\n'.join(['$ %(cmd)s\n%(res)s' % c for c in cmds])

    md(r, into=res_as if res_as else bash)
    return cmds
