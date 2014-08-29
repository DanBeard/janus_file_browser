__author__ = 'varx'


class BaseRenderer(object):
    """
    Base renderer that all renders should inherit from
    """

    def can_render(self, path):
        raise NotImplementedError()

    def render(self, path):
        raise NotImplementedError()