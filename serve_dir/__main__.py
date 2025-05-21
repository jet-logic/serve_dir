from .main import Main, arg, flag
from nanocli import AppBase


class App(AppBase):
    log_level = "INFO"

    def option(self, opt):
        if opt.pop_plain(val="DIR", doc="the root directory"):
            self.root_dir = opt.value
        elif opt.pop_bool("cgi", "c", doc="Use cgi script"):
            self.cgi = opt.value
        elif opt.pop_bool("byte_range", "r", doc="Use byte range"):
            self.byte_range = opt.value
        elif opt.pop_string("d", doc=False, val="DIR"):
            self.root_dir = opt.value
        elif opt.pop_string("p", doc="set port", val="PORT"):
            self.port = int(opt.value)
        elif opt.pop_string("b", doc="bind to address", val="X.X.X.X"):
            self.bind = opt.value
        else:
            super().option(opt)

    def start(self, **kwargs):
        return self


def main(*args):
    from . import server

    server.serve_dir(App().main().__dict__)


class App2(Main):
    root_dir: str = arg("The root directory", metavar="DIR")
    cgi: bool = flag("c", "Use cgi script", default=False)
    byte_range: bool = flag("b", "Use byte range", default=False)
    port: str = flag("p", "Set port", default=False, metavar="NUMBER")
    bind: str = flag("b", "Bind to address", default=False, metavar="X.X.X.X")

    def start(self) -> None:
        from . import server

        server.serve_dir(self.__dict__)


(__name__ == "__main__") and main()
