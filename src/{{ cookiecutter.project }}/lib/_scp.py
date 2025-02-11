"""

"""

from __future__ import annotations
from .._auto import auto
from ._with_exit_stack import with_exit_stack


@with_exit_stack
def scp(
    *args,
    verbose: bool = True,
    key: str | auto.typing.Literal[...] | None = ...,
    key_name: str = 'SSH_KEY',
       enter,
):
    if key is ...:
        key = auto.self.lib.getkey(key_name)
        key = auto.base64.b64decode(key)

    if key is not None:
        tmp = enter( auto.tempfile.TemporaryDirectory() )
        tmp = auto.pathlib.Path(tmp)

        tmp_key = tmp / 'id_rsa'
        tmp_key.write_bytes(key)
        tmp_key.chmod(0o600)

        args = [
            '-i', tmp_key,
            *args,
        ]

    canary = tmp / 'canary'
    name = f'scp-{auto.uuid.uuid4()}'

    args = [
        '-o', 'StrictHostKeyChecking=no',
        '-o', 'UserKnownHostsFile=/dev/null',
        '-o', 'BatchMode=yes',
        *args,
    ]

    args = [
        'scp',
        *args,
    ]

    print(f'$ {auto.shlex.join(map(str, args))}')

    # args = [
    #     'bash', '-c', auto.textwrap.dedent(r'''
    #         set -euo pipefail

    #         canary=${1:?}; shift
    #         onexit() { touch "${canary:?}"; }
    #         trap onexit EXIT

    #         cd /content
    #         "${@:?}"
    #     '''), '<bash -c>', *[
    #         canary,
    #     ],
    #     'tmux', 'new-window', *[
    #         '-t', f'1',
    #         '-n', name,
    #         *args,
    #     ],
    # ]

    # !{auto.shlex.join(map(str, args))}

    auto.self.lib.terminal(
        args,
        verbose = False,
    )

    # while not canary.exists():
    #     auto.time.sleep(0.1)
