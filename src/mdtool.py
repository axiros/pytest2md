"""
Postprocessing the Markdown for various Hosting Ways
"""


from functools import partial
import fnmatch
import sys, os

# replacer for shortcut curls, which can be themselves replaced by the build
# static is just a static webserver:
known_src_links = {
    'github': (
        'https://github.com/%(gh_repo_name)s/blob/%(git_rev)s/'
        '%(path)s%(line:#L%s)s'
    ),
    'github_raw': (
        'https://raw.githubusercontent.com/%(gh_repo_name)s/'
        '%(git_rev)s/%(path)s%(line:#L%s)s'
    ),
    'static': 'file://%(src_base_dir)s/%(path)s',
}
known_src_links['static_raw'] = known_src_links['static']


def info(msg, **kw):
    print(msg, kw)


valid_file = lambda f: False if f.endswith('.pyc') else True
valid_dir = lambda d: False if (d[0] in ('.', '_') or '.egg' in d) else True


def find_file(pattern, path, match=fnmatch.fnmatch):
    result = []
    for root, dirs, files in os.walk(path, topdown=True):
        dirs[:] = [d for d in dirs if valid_dir(d)]
        for name in files:
            if valid_file(name):
                if match(name, pattern):
                    result.append(os.path.join(root, name))
    return result


class InitData:
    """
    This is delivering values for keys in src_links which are not determinable
    from the markdown itself but from e.g. looking into our git config.

    Example: gh_repo_name is part of the links for github.

    All keys used in the source link templates in 'known_src_links' must be
    having a method here to find them, unless they can be delivered from the
    markdown itself..

    Todo: extend for bitbucket..., custom"""

    @staticmethod
    def src_base_dir(mdt):
        return mdt.src_base_dir

    @staticmethod
    def gh_repo_name(mdt):
        r = os.popen('cd "%s"; git remote -v' % mdt.src_base_dir).read()
        r = [l for l in r.splitlines() if 'github.com' in l and 'push' in l]
        if not r:
            raise Exception('No github push remote found. remotes=' % str(r))
        r = r[0].split('github.com', 1)[1].rsplit('.git', 1)[-2]
        if r[0] in ('/', ':'):
            r = r[1:]
        return r

    @staticmethod
    def git_rev(mdt):
        r = os.popen('cd "%s"; git rev-parse HEAD' % mdt.src_base_dir).read()
        return r.strip()


class ItemGetter:
    def __init__(self, ctx):
        self.ctx = ctx

    def __getitem__(self, k, d=None):
        c = self.ctx
        v = c.pop(k, None)
        if v:
            return v
        # %(line:#L%s)s
        if ':' in k and '%s' in k:
            k1, r = k.split(':', 1)
            if k1 in c:
                return r % c.pop(k1)
        return ''


class MDTool(object):
    md = ''
    links = {}
    autogen_links_sep = '\n\n<!-- autogenlinks -->\n'

    def __init__(self, md, src_dir, src_link_tmpl_name=None):
        self._md_file = md

        if not src_link_tmpl_name:
            # try to find from within the md itself:
            md = self._md_file.split('<!-- md_links_for:')
            if len(md) > 1:
                src_link_tmpl_name = md[1].split('--', 1)[0].strip()
        src_link_tmpl_name = src_link_tmpl_name or 'static'
        print('Rendering links for', src_link_tmpl_name)
        self.src_base_dir = src_dir
        self.src_link_tmpl_name = src_link_tmpl_name
        if not os.environ.get('NOLINKREPL'):
            self.src_link_repl_ctx = self.init_src_link_tmpl()

    def init_src_link_tmpl(self):
        """doing all we only have to do once"""

        # mdt.src_link_tmpl = 'github'
        # replace given by name with the lookup result from teh known..dict:
        name = self.src_link_tmpl_name
        self.src_link_tmpl = sl = known_src_links[name]
        self.src_link_tmpl_raw = known_src_links[name + '_raw']

        if not '/' in sl:
            raise Exception('Not supported', self.src_link_tmpl)
        ctx = self.src_url_ctx = {}
        for k in [l for l in dir(InitData) if not l.startswith('_')]:
            if k in sl:
                # adding git revision to link rednering context
                # k e.g. gh_repo_name
                ctx[k] = getattr(InitData, k)(self)
        return ctx

    def do_set_links(mdt):
        """
        Link replacer.
        Rewrites `[k1:v1,k2:v2,...]<SRC>` by replacing k1, k2,... in
        `src_link_tmpl` keys with given values.

        if a key is not in context the replacement is empty string.

        Replacement can be 1 level nested: [line:#L%s] resolves e.g. to '#L42'
        if line is present else to ''

        Special keys:
        - title: Will become the link text
        - src_base_dir: From App, for pytest the folder of the pytested file.
        - path: file path relative to src_base_dir
        - fmatch: Startswith pattern of file name in dir. Must match uniquely.
            also builds if not present:
            - path
            - title
        - lmatch: Contains match within a file
            also builds if not present:
            - line
        - gh_repo_name, git_rev: determined once at startup

        Trivial format [foo]<SRC> is ident to [fmatch:foo]<SRC>

        """
        if os.environ.get('NOLINKREPL'):
            info('Not replacing links', environ='NOLINKREPL')
            return

        md = mdorig = mdt._md_file.split(mdt.autogen_links_sep, 1)[0]
        mdparts = md.split('\n```')
        r = []
        while mdparts:
            md, fenced_code = mdparts.pop(0), None
            if mdparts:
                fenced_code = mdparts.pop(0)
            parts = md.split(']<SRC>')
            ri = []
            while parts[:-1]:
                part = parts.pop(0)
                if not '[' in part:
                    ri.append(part)
                    continue
                pre, lnk = part.rsplit('[', 1)

                title, link = mdt.build_src_link(lnk)  # <--------------- !

                if title != None:
                    ri.append('%s[%s][%s]' % (pre, title, link))
                else:
                    ri.append(part)
            assert len(parts) == 1
            ri.append(parts[0])
            r.append(''.join(ri))
            if fenced_code:
                r.append(fenced_code)
        mdr = '\n```'.join(r)
        links = mdt.links
        if not links:
            return mdorig

        mdr += mdt.autogen_links_sep
        for l in sorted(links.keys()):
            mdr += '[%s]: %s\n' % (l, links[l])

        return mdr, mdr != mdorig

    def build_src_link(mdt, lnk):
        """lnk the stuff in []"""
        # build ld: link dict, {'title', 'file', evtl. lineof...}"""
        if ':' in lnk or ',' in lnk:
            try:
                ld = to_dict(lnk)  # link dict
            except:
                return None, None
        else:
            ld = {'title': lnk, 'fmatch': lnk}

        ld['title'] = ld.get('title', ld.get('fnmatch', lnk))

        title = ld['title']
        raw = ld.pop('show_raw', 0)
        if raw:
            tmpl = mdt.src_link_tmpl_raw
        else:
            tmpl = mdt.src_link_tmpl

        if '%(path' in tmpl and not 'path' in ld:
            path = find_path(ld, bd=mdt.src_base_dir)
            if not path:
                return None, None
            ld['path'] = path

        ld['file'] = ld.get('file', ld.get('path', '').rsplit('/', 1)[-1])
        ld['fullpath'] = fn = os.path.join(mdt.src_base_dir, ld['path'])

        if '%(line' in tmpl and not 'line' in ld:
            if 'lmatch' in ld:
                match = ld['lmatch']
                with open(fn, 'r') as fd:
                    for (i, line) in enumerate(fd):
                        if match in line:
                            ld['line'] = str(i)
                            break

        link = ld['file']
        ctx = dict(mdt.src_link_repl_ctx)
        ctx.update(ld)
        mdt.links[link] = tmpl % ItemGetter(ctx)

        return title, link

    def make_toc(mdt, md):
        """making a table of content, replacing "[TOC]" -else at the beginning"""
        T = '\n[TOC]\n'
        if not T in md:
            md = T + md
        pre, md = md.split(T)
        from pytest_to_md import strutils

        lines = md.splitlines()
        toc = ['']
        r = []
        while lines:
            line = lines.pop(0)
            r.append(line)
            for code in '```', '    ':
                if line.startswith(code):
                    while True:
                        r.append(lines.pop(0))
                        if r[-1].startswith(code):
                            break
            if line.startswith('#'):
                lev, h = line.split(' ', 1)
                toc.append(
                    '    ' * (len(lev) - 1)
                    + '- [%s](#%s)' % (h, strutils.slugify(h, delim='-'))
                )
        toc.append('')
        toc.extend(r)
        res = pre + '\n'.join(toc)
        return res


def find_path(ld, bd):
    """link dict, base dir"""
    file = ld.get('fmatch')
    if not file:
        return
    found = find_file(file + '*', bd)
    if len(found) == 0:
        print('Not found', file, 'from', ld, 'builddir', bd)
        return
    elif len(found) > 1:
        found = [f for f in found if f.rsplit('/', 1)[-1] == file]
        if len(found) != 1:
            return
            # info('No unique source link found')
    if len(found) == 1:
        return found[0][len(bd) + 1 :]


def to_dict(s):
    l = [kv.strip().split(':', 1) for kv in s.split(',')]
    return dict([(k.strip(), v.strip()) for k, v in l])
