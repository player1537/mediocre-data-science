"""

"""

from __future__ import annotations
from .._auto import auto
from ._with_exit_stack import with_exit_stack


@with_exit_stack
def checksum(
    *,   enter,
    path: auto.pathlib.Path | None = None,
    hash: str | auto.typing.Literal[...] | None = None,

    verbose: bool = True,
):
    if not hasattr(path, 'open'):
        path = auto.pathlib.Path(path)

    pbar = enter( auto.tqdm.auto.tqdm(
        leave=False,
        total=int(path.stat().st_size),
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        desc='Checksum',
    ) )

    h = auto.hashlib.new('sha256')
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            if verbose:
                pbar.update(len(chunk))

            h.update(chunk)

    h = h.hexdigest()
    assert h == hash, f'Invalid checksum: {h!r}'
