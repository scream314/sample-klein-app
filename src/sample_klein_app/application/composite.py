"""
Composite application
"""

from twisted.web.iweb import IRequest

from ._main import main
from .klein import Klein, KleinRenderable
from .dns import Application as DNSApplication
from .hello import Application as HelloApplication
from .math import Application as MathApplication


__all__ = (
    "Application",
)


class Application(object):
    """
    Composite application.

    Application that exposes endpoints that are handled by other applications,
    thereby composing multiple applications into a single application.
    """

    router = Klein()

    main = classmethod(main)  # type: ignore

    @router.route("/")
    def root(self, request: IRequest):
        """
        Application root resource.

        Responds with a message noting the nature of the application.

        @param request: The request to respond to.
        """
        return "This is a web application composed from multiple applications."

    @router.route("/dns/", branch=True)
    def dns(self, request: IRequest):
        """
        DNS application resource.

        Routes requests to L{DNSApplication}.

        @param request: The request to respond to.
        """
        return DNSApplication().router.resource()

    @router.route("/hello/", branch=True)
    def hello(self, request: IRequest):
        """
        Hello application resource.

        Routes requests to L{HelloApplication}.

        @param request: The request to respond to.
        """
        return HelloApplication().router.resource()

    @router.route("/math/", branch=True)
    def math(self, request: IRequest):
        """
        Math application resource.

        Routes requests to L{MathApplication}.

        @param request: The request to respond to.
        """
        return MathApplication().router.resource()


if __name__ == "__main__":  # pragma: no cover
    Application.main()  # type: ignore
