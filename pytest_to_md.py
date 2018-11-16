"""
Creates markdown - while testing contained code snippets.

"""
import inspect
import subprocess as sp
import pytest
import os
import time
import pdb
from ast import literal_eval as ev

if not hasattr(sp, 'getoutput'):
    # adding the convenient PY3 getoutput to sp.
    # hope correct (in plane, offline):
    import subprocess as sp

    def _(*a, **kw):
        kw['stdout'] = sp.PIPE
        kw['stderr'] = sp.PIPE
        kw['shell'] = True
        out, err = sp.Popen(*a, **kw).communicate()
        if out.endswith('\n'):
            out = out[:-1]
        return out + err

    sp.getoutput = _

# also py2 compat:
breakpoint = pdb.set_trace

# contains the config, populated in setup:
cfg = {}

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

    cfg['md_sep'] = md_sep
    fnt = fn_test_file
    here = cfg['here'] = DIR(fnt)
    if not fn_readme:
        fn = cfg['fn_readme'] = DIR(here) + '/README.md'

    if not os.path.exists(fn):
        print('Creating', fn)
        with open(fn, 'w') as fd:
            fd.write('\n'.join(('', md_sep, 'will be autogened.', md_sep, '')))

    name = cfg['name'] = rpl(fn_test_file.rsplit('/', 1)[-1], 'test_', '.py')
    cfg['d_assets'] = here + '/' + name + '/'
    fn_md = cfg['fn_md'] = here + '/' + name + '.md'

    if os.path.exists(fn_md):
        os.unlink(fn_md)
    with open(fn_md, 'w') as fd:
        fd.write('')

    return here, fn_md


def write_readme():
    """
    addd the new version of the rendered tutorial into the main readme
    """
    fn = cfg['fn_md']
    with open(fn) as fd:
        tut = fd.read()

    fnr = cfg['fn_readme']
    with open(fnr) as fd:
        readm = fd.read()
    m = cfg['md_sep']
    pre, _, post = readm.split(m)
    with open(fnr, 'w') as fd:
        fd.write(''.join((pre, m, tut, '\n', m, post)))


code = """```code
%s
```"""
# fmt: off
nothing  = lambda s: s
python   = lambda s: code.replace('code', 'python')   % s
bash     = lambda s: code.replace('code', 'bash')     % s
markdown = lambda s: code.replace('code', 'markdown') % (s.replace('```', "``"))
as_lang  = lambda s, lang: code.replace('code', lang) % s
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

        ff = '<from_file: '
        if l.strip().startswith(ff):
            pre, post = l.split(ff, 1)
            fn, post = post.rsplit('>', 1)
            if not fn.startswith('/'):
                fn = cfg['d_assets'] + fn
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
    fn = cfg['fn_md']
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
    D = cfg['d_assets']

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


exists = os.path.exists


def sh_file(fn, lang='python', content=None):
    ex = exists(fn)
    if not ex and not content:
        raise Exception('not found', fn)
    dn = os.path.dirname(fn)
    if not exists(dn):
        os.system('mkdir -p "%s"' % dn)
    if content:
        with open(fn, 'w') as fd:
            fd.write(content)
    else:
        with open(fn) as fd:
            content = fd.read()
    FN = os.path.abspath(fn).rsplit('/', 1)[1]
    content = ('$ cat "%s"' % FN) + '\n' + content
    content = as_lang(content, lang)
    md(content)


def sh_code(func):
    return md(python(inspect.getsource(func)))


# .
