"""
Creates markdown - while testing contained code snippets.

"""
from ast import literal_eval as ev
from pytest2md import strutils
from pytest2md import mdtool
import subprocess as sp
import inspect
import pytest
import os
import time
import pdb


exists = os.path.exists
abspath = os.path.abspath
dirname = os.path.dirname

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

DIR = lambda d: abspath(dirname(d))


def rpl(what, *with_):
    for w in with_:
        if not isinstance(w, (tuple, list)):
            w = (w, '')
        what = what.replace(w[0], w[1])
    return what


def convert_to_staticmethods(cls):
    """Helper for Py2 - in docu we often use classes as namespaces"""
    meths = [(k, getattr(cls, k)) for k in dir(cls)]
    c = callable
    meths = [(k, meth) for k, meth in meths if k[:2] != '__' and c(meth)]
    [setattr(cls, k, staticmethod(f)) for k, f in meths]


def setup(
    fn_test_file, fn_target_md=None, md_sep=dflt_md_sep, fn_target_md_tmpl=None
):
    """
    called at module level by pytest test module, which creates the md
    e.g. fn_test_file=/Users/gk/GitHub/pytest2md/tests/test_tutorial.py

    - fn_target_md: The final rendered result file. Default: HERE/README.md
    - md_sep: A seperator where we fill in the mardkown from the pytest
    - fn_target_md_tmpl: A template file, containing the static md around the seps.
                    If not given we replace the content at every pytest run in
                    fn_target_md itself.
                    This is useful when you edit a lot in markdown and don't want
                    clutter from the autogen result in that file.
    Filenames relative to directory of fn_test_file or absolut.

    In this setup function we generate e.g. this as config:
    (Pdb) pp cfg (for a run of our own tutorial)
    {'d_assets'         : '/data/root/pytest2md/tests/tutorial/',
    'fn_md'             : '/data/root/pytest2md/tests/tutorial.md',
    'fn_target_md'      : '/data/root/pytest2md/README.md.tmpl',
    'here'              : '/data/root/pytest2md/tests',
    'md_sep'            : '<!-- autogen tutorial -->',
    'name'              : 'tutorial',
    'fn_target_md_tmpl' : '/data/root/pytest2md/README.md.tmpl'}
    """
    cfg['md_sep'] = md_sep
    cfg['here'] = here = DIR(fn_test_file)

    # assuming tests in <base>/tests:
    if not fn_target_md:
        fn_target_md = here + '/../README.md'

    if not fn_target_md.startswith('/'):
        fn_target_md = abspath(cfg['here'] + '/' + fn_target_md)
    fn = cfg['fn_target_md'] = fn_target_md

    dflt_tmpl = fn.replace('.md', '.tmpl.md')
    if os.path.exists(dflt_tmpl) and not fn_target_md_tmpl:
        fn_target_md_tmpl = dflt_tmpl
    if not fn_target_md_tmpl:
        print(
            'Replacing content in the final markdown, no template',
            cfg['fn_target_md'],
        )
        fn_target_md_tmpl = cfg['fn_target_md']
    cfg['fn_target_md_tmpl'] = fn_target_md_tmpl

    fn = fn_target_md_tmpl
    if not exists(fn):
        print('Creating', fn)
        with open(fn, 'w') as fd:
            fd.write('\n'.join(('', md_sep, 'will be autogened.', md_sep, '')))

    name = cfg['name'] = rpl(fn_test_file.rsplit('/', 1)[-1], 'test_', '.py')
    cfg['d_assets'] = here + '/' + name + '/'

    def create_empty_md_file(name):
        here = cfg['here']
        # create
        fn_md = cfg['fn_md'] = here + '/' + name + '.md'
        if exists(fn_md):
            os.unlink(fn_md)
        with open(fn_md, 'w') as fd:
            fd.write('')
        return fn_md

    fn_md = create_empty_md_file(name)
    # returns e.g.
    # /data/root/pytest2md/tests /data/root/pytest2md/tests/tutorial.md
    # pytest will create fn_md from scratch, which will be put at write_readme
    # into the template, which will be after replacements go into md_target
    return here, fn_md


#
#    def get_repo_base_url(dvcs):
#        url = dvcs  # just for the error, once we have hg it'll be sane
#        if dvcs == 'git':
#            url = os.popen('git config --get remote.origin.url').read().strip()
#            if 'github' in url:
#                url, post = url.rsplit('.git', 1)
#                assert not post
#                pre, post = url.rsplit('/', 1)
#                pre = pre.rsplit('/', 1)[-1].rsplit(':', 1)[-1]
#                cfg['repo_path'] = pre + '/' + post
#                return repo_urls['github']
#        raise NotImplemented('Repo url for dvcs', dvcs, url)
#
#    def set_repo_base_url(rbu):
#        dvcss = {'git': None, 'hg': None}
#        if rbu == None:
#            d = cfg['here']
#            for dvcs in dvcss.keys():
#                while not exists(d + '/.' + dvcs) and d != '/':
#                    d = dirname(d)
#                if d != '/':
#                    dvcss[dvcs] = get_repo_base_url(dvcs)
#                    break
#
#        breakpoint()
#
#    set_repo_base_url(repo_base_url)
#
# repo_urls = {
#    'github': 'https://github.com/%(repo_path)s/blob/%(repo_rev)s/%(file_path)s#L%(file_line)s'
# }
#


def write_readme(with_source_ref=False, make_toc=False):
    """
    addd the new version of the rendered tutorial into the main readme
    """
    # export DIR_SRC="https://github.com/axiros/DevApps/blob/`git rev-parse  HEAD`/"
    # fn_md is created from the pytest:
    src = sys._getframe().f_back.f_code
    fn = cfg['fn_md']
    with open(fn) as fd:
        tut = fd.read()
    if with_source_ref:
        tut += dedent(
            """

        *Auto generated by [pytest2md](https://github.com/axiros/pytest2md), running [%s]<SRC>*
        """
            % src.co_filename.rsplit('/', 1)[-1]
        )

    fnr = cfg['fn_target_md_tmpl']
    with open(fnr) as fd:
        readm = fd.read()
    # something like <! autoconf...:
    m = cfg['md_sep']
    pre, _, post = readm.split(m)
    md = ''.join((pre, m, tut, '\n', m, post))
    print('Now postprocessing', cfg['fn_target_md'])
    d = dirname(cfg['fn_target_md'])
    mdt = mdtool.MDTool(
        md=md, src_dir=d, src_link_tmpl_name=os.environ.get('MD_LINKS_FOR')
    )
    md, changed = mdt.do_set_links()
    if make_toc:
        md = mdt.make_toc(md)
    with open(cfg['fn_target_md'], 'w') as fd:
        fd.write(md)


# ------------------------------------------------------- Creating the Markdown

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

import sys
import inspect


class Printed:
    stdout = []
    stderr = []

    @staticmethod
    def write(*a):
        Printed.stdout.extend(list(a))


def run_and_document_pyfunc(funcstr, frame):
    func = frame.f_locals[funcstr]
    s = inspect.getsource(func).split(':', 1)[1]
    s = deindent(s)
    # if the function is called outside (to test asserttions) then it'll end
    # with a return - we omit that, if the user wants the reader to see the
    # assertion he should put it inside the func:
    pre, last = s.rsplit('\n', 1)
    if last.lstrip().startswith('return '):
        s = pre
    # wrap into python code block:
    s = python(s)
    del Printed.stdout[:]  # py2, no clear
    del Printed.stderr[:]  # py2, no clear
    try:
        o = sys.stdout
        e = sys.stderr
        if not 'breakpoint' in s:
            sys.stdout = Printed
            sys.stderr = Printed
        func()
    finally:
        sys.stdout = o
        sys.stderr = e
    so = ''.join(Printed.stdout)
    if so:
        if so.startswith('MARKDOWN:'):
            so = so.replace('MARKDOWN:', '\n')
        elif not so.lstrip().startswith('```'):
            so = '\nOutput:\n```\n' + so + '\n```'
        s += so
    return s + '\n'


def deindent(p):
    pp = p.replace('\n', '')
    ind = len(pp) - len(pp.lstrip())
    if not ind:
        return p
    return '\n'.join(
        [l[ind:] if not l[:ind].strip() else l for l in p.splitlines()]
    )


import json
from textwrap import dedent


def as_json(d):
    if not isinstance(d, str):
        d = json.dumps(d, sort_keys=True, default=str, indent=4)
    return 'MARKDOWN:\n\n```javascript\n%s\n```' % d


# *headers is not py2 compatible :-(
def html_table(list, headers, summary=None):
    """ A tool which test pythons' may use to format their func results"""
    p = '</td><td>'
    row = lambda r: '<tr><td>' + r + '</td></tr>'
    r = (row(p.join(headers)),)
    for l in list:
        r += (row(p.join(l)),)
    r = '<table>\n' + '\n'.join(r) + '\n</table>'
    if summary:
        r = """<details>
        <summary>%s</summary>
        %s
        </details>
        """ % (
            summary,
            r,
        )

    return 'MARKDOWN:\n\n' + r


def md_from_source_code():
    src = sys._getframe().f_back
    mdsrc = dedent(inspect.getsource(src.f_code).split(':', 1)[1])
    apos = mdsrc.lstrip()[:3]  # ''' or """
    parts = mdsrc.split('\n' + apos + '\n')
    r = parts.pop(0)
    while parts:
        part = parts.pop(0)
        if parts:
            func = parts.pop(0)
            try:
                funcname = func.lstrip().split('def ', 1)[1].split('(', 1)[0]
            except Exception as ex:
                continue
            part += '\npyrun: %s\n' % funcname
        r += part
    md(r, test_func=src)


def md(paras, into=nothing, test_func=None):
    """writes markdown"""
    paras = [paras]
    lctx = {}
    lctx['in_code_block'] = False

    paras = [deindent(p) for p in paras]
    test_func = test_func or sys._getframe().f_back
    parts = paras[0].split('pyrun: ')
    after = parts.pop(0)
    while parts:
        part = parts.pop(0)
        func, post = part.split('\n', 1)
        after += run_and_document_pyfunc(func, test_func) + post

    paras = [after]

    def repl(l, lctx=lctx):
        if '```' in l:
            lctx['in_code_block'] = not lctx['in_code_block']

        ff = '<from_file: '
        if l.strip().startswith(ff):
            pre, post = l.split(ff, 1)
            fn, post = post.rsplit('>', 1)
            if not fn.startswith('/'):
                fn = cfg['d_assets'] + fn
            if not exists(fn):
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


def sh_file(fn, lang='python', content=None):
    ex = exists(fn)
    if not ex and not content:
        raise Exception('not found', fn)
    dn = dirname(fn)
    if not exists(dn):
        os.system('mkdir -p "%s"' % dn)
    if content:
        with open(fn, 'w') as fd:
            fd.write(content)
    else:
        with open(fn) as fd:
            content = fd.read()
    FN = abspath(fn).rsplit('/', 1)[1]
    content = ('$ cat "%s"' % FN) + '\n' + content
    content = as_lang(content, lang)
    md(content)


def sh_code(func):
    return md(python(inspect.getsource(func)))


# .
