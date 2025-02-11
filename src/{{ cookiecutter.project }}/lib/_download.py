"""

"""

from __future__ import annotations
from .._auto import auto
from ._with_exit_stack import with_exit_stack


@with_exit_stack
def download(
    *,   enter,
    path: auto.pathlib.Path | str = None,
    href: str = None,
    root: auto.pathlib.Path | auto.typing.Literal[...] = ...,

    verbose: bool = True,

    tmp_path: auto.pathlib.Path | auto.typing.Literal[...] = ...,
    tmp_root: auto.pathlib.Path | auto.typing.Literal[...] = ...,
    tmp_name: str = 'download.tmp',
) -> auto.pathlib.Path:
    if isinstance(path, str):
        path = auto.pathlib.Path(path)
    
    if root is ...:
        root = path.parent

    if tmp_path is ...:
        if tmp_root is ...:
            tmp_root = root
        tmp_path = tmp_root / tmp_name

    r = enter( auto.requests.request(
        'GET',
        href,
        stream=True,
    ) )
    r.raise_for_status()

    if verbose:
        pbar = enter( auto.tqdm.auto.tqdm(
            total=int(r.headers.get('Content-Length', 0)),
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            desc='Download',
        ) )

    with tmp_path.open('wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            if verbose:
                pbar.update(len(chunk))

            f.write(chunk)

    tmp_path.rename(path)
    assert path.exists(), path

    return path
