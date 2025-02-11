"""

"""

from __future__ import annotations
from .._auto import auto
from ._with_exit_stack import with_exit_stack


@with_exit_stack
def terminal(
    args: str | list,
    *,   enter,
    verbose: bool = True,
    session: str = '4Y07PNNCK031RJN3MXFD2YKHPP',
) -> None:
    tmpdir = enter( auto.tempfile.TemporaryDirectory() )
    tmpdir = auto.pathlib.Path(tmpdir)

    has_tmux = auto.shutil.which('tmux') is not None

    canary = tmpdir / '__terminal_canary'


    if isinstance(args, str):
        if verbose:
            print('$', args)

        args = ['bash', '-c', args, '<bash -c>']

    else:
        if verbose:
            print('$', auto.shlex.join(map(str, args)))

    assert isinstance(args, list), type(args)

    args = [
        'bash', '-c', (
            r'''onexit() { touch "${canary:?}"; }; '''
            r'''canary=${1:?}; shift; '''
            r'''trap onexit EXIT; '''
            r'''"${@:?}"'''
        ), '<bash -c>', *[
            canary,
            *args,
        ],
    ]

    if isinstance(args, list):
        args = auto.shlex.join(map(str, args))
    assert isinstance(args, str), type(args)

    if has_tmux:
        process = auto.subprocess.run([
            'tmux', 'list-sessions', '-F', '#{session_name}',
        ], stdin=auto.subprocess.DEVNULL, stdout=auto.subprocess.PIPE, check=False)
        
        sessions = set(process.stdout.decode().splitlines())

        if session not in sessions:
            try:
                get_ipython
            except NameError:
                auto.subprocess.run([
                    'tmux', 'new-session', '-d', '-s', session,
                ], check=True)
            else:
                get_ipython().system('tmux new-session -d -s {session}')

    if has_tmux:
        args = [
            'tmux', 'send-keys', *[
                '-t', session,
                ' ',
                args,
                'C-m',
            ],
        ]
    else:
        args = [
            'bash', '-c', args,
        ]

    try:
        get_ipython
    except NameError:
        auto.subprocess.run(
            args,
            check = True,
        )
    else:
        get_ipython().system('{auto.shlex.join(args)}')

    while True:
        if canary.exists():
            break

        auto.time.sleep(0.1)

    canary.unlink()
