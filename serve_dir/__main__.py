from .main import Main, arg, flag, _arg_fields


class App(Main):
    root_dir: str = arg(
        "The root directory", metavar="DIR", default=".", required=False
    )
    cgi: bool = flag("cgi", "Use cgi script", default=None)
    byte_range: bool = flag("byte-range", "Use byte range", default=None)
    port: int = flag("p", "Set port", metavar="NUMBER", default=8058)
    bind: str = flag("b", "Bind to address", metavar="X.X.X.X", default="0.0.0.0")

    def start(self) -> None:
        from .server import serve_dir

        print(self.__dict__)
        for x in _arg_fields(self):
            print(x, x[1] is not bool)
            # print(issubclass(x[1], (int, float, str)))

        serve_dir(self.__dict__)


(__name__ == "__main__") and App().main()
