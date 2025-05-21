from os import fstat, stat


def get_file_stream(path):
    if ".parts.json." in path:
        f = Segments(path)
        return (f, f.length, stat(path).st_mtime)
    else:
        f = open(path, "rb")
        s = fstat(f.fileno())
        return (f, s.st_size, s.st_mtime)


class Segments(object):
    def __init__(self, src):
        from os.path import realpath, abspath, dirname

        self.pos = 0
        with open(src, "rb") as h:
            from json import load

            m = load(h)
            folder = dirname(realpath(abspath(src)))
            self.length = m["length"]
            self.parts = sorted(
                [x[0], x[1], resolve_source(x[2], folder), None] for x in m["parts"]
            )
        from sys import stdout

        self.log = stdout.write

    def tell(self):
        assert self.pos < self.length
        assert self.pos >= 0
        return self.pos

    def close(self):
        out = self.log
        for x in self.parts:
            f = x[3]
            if f:
                out("DONE %s-%s %r\n" % (x[0], x[1], x[3]))
                x[3] = f.close() and None
        self.pos = 0
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def seek(self, offset, whence=0):
        assert self.pos < self.length
        assert self.pos >= 0
        if whence == 0:
            assert offset < self.length
            assert offset >= 0
            new_pos = self.pos = offset
        elif whence == 1:
            assert (self.pos + offset) < self.length
            assert (self.pos + offset) >= 0
            new_pos = self.pos = self.pos + offset
        elif whence == 2:
            assert (self.length + offset) < self.length
            assert (self.length + offset) >= 0
            new_pos = self.pos = self.length + offset
        else:
            assert 0
        return new_pos

    def read(self, n):
        pos = self.pos
        out = self.log
        assert pos >= 0
        for x in self.parts:
            (s, e, path, f) = x
            assert e > s
            if pos >= s and pos < e:
                seek = pos - s
                size = min(e - pos, n)
                if not f:
                    out("OPEN %s-%s %r\n" % (x[0], x[1], x[2]))
                    x[3] = f = open(path, "rb")
                f.seek(seek)
                b = f.read(size)
                size = len(b)
                pos += size
                n -= size
                self.pos = pos
                return b
            else:
                if f:
                    out("done %s-%s %r\n" % (x[0], x[1], x[3]))
                    x[3] = f.close() and None
        out("hole %s-%s\n" % (pos, pos + n))
        pos += n
        self.pos = pos
        return b"\x00" * n


from os.path import isabs, abspath, normpath, join
from urllib.request import url2pathname
from urllib.parse import urlparse


def resolve_source(uri, dirParent, pathIdTup=None):
    # (scheme, netloc, path, params, query, fragment)
    url = urlparse(uri)
    path = url2pathname(url[2])
    if isabs(path):
        path = abspath(path)
    else:
        path = normpath(join(dirParent, path))
    if pathIdTup:
        return (path, url[5])
    return path
