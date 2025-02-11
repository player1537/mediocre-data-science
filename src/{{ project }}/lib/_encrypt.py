"""

"""

from __future__ import annotations
from .._auto import auto
from ._with_exit_stack import with_exit_stack


@with_exit_stack
def encrypt(
    *,   enter,

    dec_path: auto.os.PathLike,

    password: str | auto.typing.Literal[...] = ...,
    password_name: str | None = None,

    verbose: bool = True,

    enc_path: auto.os.PathLike | auto.typing.Literal[...] = ...,
    enc_root: auto.pathlib.Path | auto.typing.Literal[...] = ...,
    enc_name: str | auto.typing.Literal[...] = ...,

    tmp_path: auto.pathlib.Path | auto.typing.Literal[...] = ...,
    tmp_root: auto.pathlib.Path | auto.typing.Literal[...] = ...,
    tmp_name: str = 'encrypt.tmp',
) -> auto.pathlib.Path:
    dec_path = auto.pathlib.Path(dec_path)

    if enc_path is ...:
        if enc_root is ...:
            enc_root = dec_path.parent
        if enc_name is ...:
            enc_name = f'{dec_path.name}.enc'
        enc_path = enc_root / enc_name
    else:
        enc_path = auto.pathlib.Path(enc_path)

    if password is ...:
        password = auto.self.lib.getkey(password_name)
    assert password is not None

    if tmp_path is ...:
        if tmp_root is ...:
            tmp_root = enc_path.parent
        tmp_path = tmp_root / tmp_name

    if verbose:
        pbar = enter( auto.tqdm.auto.tqdm(
            total=int(dec_path.stat().st_size),
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            desc='Encrypt',
        ) )

    p = enter( auto.subprocess.Popen([
        'openssl', 'enc',
        '-aes-256-ctr',
        '-pbkdf2',
        '-md', 'sha-256',
        # '-in', enc_path,
        '-out', tmp_path,
        '-pass', f'pass:{password}',
    ], stdin=auto.subprocess.PIPE) )

    with dec_path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            if verbose:
                pbar.update(len(chunk))

            p.stdin.write(chunk)

    p.stdin.close()
    p.wait()
    assert p.returncode == 0, p.returncode

    tmp_path.rename(enc_path)
    assert enc_path.exists(), enc_path

    return enc_path
