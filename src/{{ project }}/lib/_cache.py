"""

"""

from __future__ import annotations
from .._auto import auto


_cachecache = {}


class Cache:
    def __new__(
        cls,
        *,
        path: auto.pathlib.Path | auto.typing.Literal[...] = ...,
        root: auto.pathlib.Path,
        name: str = (
            'Cache.sqlite3.enc'
        ),
    ):
        if path is ...:
            path = root / name
        
        ckey = path
        if ckey not in _cachecache:
            self = super().__new__(cls)
            self.path = path
            self.conn = auto.sqlite3.connect(
                ':memory:',
                check_same_thread = False,
            )
            auto.self.lib.attach(
                self.conn,
                path,
                name = 'Cache',
                mode = 'rwc',
            )
            
            self.conn.execute(auto.self.lib.SQLQuery(r'''
                CREATE TABLE IF NOT EXISTS Cache.Cache (
                    key TEXT PRIMARY KEY,
                    value BLOB
                )
            '''))
            
            self.conn.commit()
            
            _cachecache[path] = self
            return self

        else:
            self = _cachecache[ckey]

        return self

    def __getitem__(self, key: str) -> auto.typing.Any:
        with auto.contextlib.closing(self.conn.execute(auto.self.lib.SQLQuery(r'''
            SELECT value
            FROM Cache
            WHERE key = ?
        '''), [key])) as cursor:
            row = cursor.fetchone()
            if row is None:
                raise KeyError(key)
            
            val = row[0]
            with auto.io.BytesIO(val) as f:
                val = auto.pickle.load(f)
            
            return val
    
    def __setitem__(self, key: str, value: auto.typing.Any):
        with auto.io.BytesIO() as f:
            auto.pickle.dump(value, f)
            val = f.getvalue()
        
        self.conn.execute(auto.self.lib.SQLQuery(r'''
            INSERT OR REPLACE INTO Cache (
                key,
                value
            ) VALUES (
                ?
                , ?
            )
        '''), [key, val])

        self.conn.commit()
    
    def __len__(self) -> int:
        with auto.contextlib.closing(self.conn.execute(auto.self.lib.SQLQuery(r'''
            SELECT COUNT(*)
            FROM Cache
        '''))) as cursor:
            row = cursor.fetchone()
            return row[0]

    def __contains__(self, key: str) -> bool:
        with auto.contextlib.closing(self.conn.execute(auto.self.lib.SQLQuery(r'''
            SELECT 1
            FROM Cache
            WHERE key = ?
        '''), [key])) as cursor:
            row = cursor.fetchone()
            return row is not None

    def clear(self):
        self.conn.execute(auto.self.lib.SQLQuery(r'''
            DELETE FROM Cache
        '''))
        self.conn.commit()
