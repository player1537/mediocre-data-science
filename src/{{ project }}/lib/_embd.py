"""

"""

from __future__ import annotations
from .._auto import auto


def embd() -> NotImplemented:
    raise NotImplementedError


def embd_dumps(arg: auto.typing.Any) -> str:
    return _embd_dumps(arg)

embd.dumps = embd_dumps


def embd_loads(arg: str) -> auto.typing.Any:
    return _embd_loads(arg)

embd.loads = embd_loads


@auto.functools.singledispatch
def _embd_dumps(arg):
    raise NotImplementedError


@_embd_dumps.register(auto.np.ndarray)
def _embd_dumps_ndarray(v: auto.np.ndarray) -> str:
    v = v.astype('f2')
    b = v.tobytes()
    s = auto.base64.b64encode(b).decode()
    return s


@_embd_dumps.register(auto.pd.Series)
def _embd_dumps_series(ds: auto.pd.Series) -> auto.pd.Series:
    ds = ds.apply(embd.dumps)
    return ds


@auto.functools.singledispatch
def _embd_loads(arg):
    raise NotImplementedError


@_embd_loads.register(str)
def _embd_loads_str(s: str) -> auto.np.ndarray:
    b = auto.base64.b64decode(s)
    v = auto.np.frombuffer(b, dtype='f2')
    v = v.astype('f4')
    return v


@_embd_loads.register(auto.pd.Series)
def _embd_loads_series(ds: auto.pd.Series) -> auto.pd.Series:
    ds = ds.apply(embd.loads)
    return ds


@_embd_loads.register(auto.np.ndarray)
def _embd_loads_ndarray(v: auto.np.ndarray) -> auto.np.ndarray:
    N = len(v)
    E = len(embd.loads(v[0]))

    ret = auto.np.empty((N, E), dtype='f4')
    for ι, vᵢ in enumerate(v):
        ret[ι, :] = embd.loads(vᵢ)

    return ret
