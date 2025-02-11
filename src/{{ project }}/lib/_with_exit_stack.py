"""

"""

from __future__ import annotations
from .._auto import auto
from .._config import config


def with_exit_stack(func, /):
    signature = auto.inspect.signature(func)

    @auto.functools.wraps(func)
    def wrapper(*args, **kwargs):
        with auto.contextlib.ExitStack() as stack:
            if 'stack' in signature.parameters:
                kwargs = kwargs | dict(stack=stack)
            if 'enter' in signature.parameters:
                kwargs = kwargs | dict(enter=stack.enter_context)
            if 'defer' in signature.parameters:
                kwargs = kwargs | dict(defer=stack.callback)

            return func(*args, **kwargs)

    return wrapper
