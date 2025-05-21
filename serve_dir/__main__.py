from .main import Main, arg, flag


class App(Main):
    root_dir: str = arg("The root directory", metavar="DIR", default=".")
    cgi: bool = flag("c", "Use cgi script", default=False)
    byte_range: bool = flag("r", "Use byte range", default=False)
    port: int = flag("p", "Set port", metavar="NUMBER", default=8058)
    bind: str = flag("b", "Bind to address", metavar="X.X.X.X", default="0.0.0.0")

    def start(self) -> None:
        from . import server

        server.serve_dir(self.__dict__)


(__name__ == "__main__") and App().main()
