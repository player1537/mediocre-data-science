"""

"""

from __future__ import annotations
from .._auto import auto
from ._with_exit_stack import with_exit_stack


@with_exit_stack
def decrypt(
    *,   enter,
    verbose: bool = True,

    enc_path: auto.os.PathLike,

    password: str | auto.typing.Literal[...] = ...,
    password_name: str | None = None,

    dec_path: auto.os.PathLike,
    dec_root: auto.pathlib.Path | auto.typing.Literal[...] = ...,
    dec_name: str | auto.typing.Literal[...] = ...,

    tmp_path: auto.pathlib.Path | auto.typing.Literal[...] = ...,
    tmp_root: auto.pathlib.Path | auto.typing.Literal[...] = ...,
    tmp_name: str = 'decrypt.tmp',
) -> auto.pathlib.Path:
    enc_path = auto.pathlib.Path(enc_path)

    if dec_path is ...:
        if dec_root is ...:
            dec_root = enc_path.parent
        if dec_name is ...:
            dec_name = enc_path.name.removesuffix('.enc')
        dec_path = dec_root / dec_name
    else:
        dec_path = auto.pathlib.Path(dec_path)

    if password is ...:
        password = auto.self.lib.getkey(password_name)
    assert password is not None

    if tmp_path is ...:
        if tmp_root is ...:
            tmp_root = dec_path.parent
        tmp_path = tmp_root / tmp_name

    if verbose:
        pbar = enter( auto.tqdm.auto.tqdm(
            total=int(enc_path.stat().st_size),
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            desc='Decrypt',
        ) )

    p = enter( auto.subprocess.Popen([
        'openssl', 'enc',
        '-d',
        '-aes-256-ctr',
        '-pbkdf2',
        '-md', 'sha-256',
        '-out', tmp_path,
        '-pass', f'pass:{password}',
    ], stdin=auto.subprocess.PIPE) )

    with enc_path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            if verbose:
                pbar.update(len(chunk))

            p.stdin.write(chunk)

    p.stdin.close()
    p.wait()
    assert p.returncode == 0, p.returncode

    tmp_path.rename(dec_path)
    assert dec_path.exists(), dec_path

    return dec_path
