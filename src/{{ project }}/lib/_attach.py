"""
A context manager for attaching encrypted SQLite databases.

Parameters:
    conn: sqlite3.Connection
        The database connection to attach to
    path: pathlib.Path
        Path to the encrypted database file
    name: str = ...
        Name to use for the attached database. If not provided, will use the 
        first part of the filename (before any commas)
    pass_: str = ...
        Decryption password. If not provided, will be retrieved from environment
        using pass_name
    pass_name: str = 'ECAMP_ENCRYPTION_KEY'
        Environment variable name to use for password
    **opts:
        Additional SQLCipher options. Defaults include 'chacha20' cipher and
        read-only mode.

Examples:
    with attach(
        conn, 
        path=path,
        name='mydb',
    ) as attach:
        conn.execute('SELECT * FROM mydb.table...')
"""

from __future__ import annotations
from .._auto import auto


class attach:
    def __init__(
        self,
        conn: auto.sqlite3.Connection,
        path: auto.pathlib.Path,
        *,
        name: str | auto.typing.Literal[...] = ...,
        pass_: str | auto.typing.Literal[...] = ...,
        pass_name: str = (
            'ECAMP_ENCRYPTION_KEY'
        ),
        **opts,
    ):
        if name is ...:
            name = arg1.name.split(',', 1)[0]
        
        if pass_ is ...:
            pass_ = auto.self.lib.getkey(pass_name)

        opts = opts.copy()
        if 'cipher' not in opts:
            opts['cipher'] = 'chacha20'
        if 'key' not in opts:
            opts['key'] = pass_
        if 'mode' not in opts:
            opts['mode'] = 'ro'
        
        scheme = 'file'
        opts = auto.urllib.parse.urlencode(opts)
        href = auto.urllib.parse.urlunparse((scheme, '', str(path), '', opts, ''))
        
        self.conn = conn
        self.name = name
        
        try:
            self.conn.execute(auto.self.lib.SQLQuery(r'''
                ATTACH DATABASE {{ href |tosqlstr }} AS {{ name |tosqlref }}
            ''', href=href, name=name))
        except auto.sqlite3.DatabaseError as e:
            raise auto.sqlite3.DatabaseError(f'Failed to attach database {name!r} from {path!r}') from e

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.execute(auto.self.lib.SQLQuery(r'''
            DETACH DATABASE {{ name |tosqlref }}
        ''', name=self.name))
