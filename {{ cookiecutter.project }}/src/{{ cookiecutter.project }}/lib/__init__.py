"""

"""

from __future__ import annotations


class _AutoImport:
    def __getattr__(self, name: str):
        raise AttributeError(f"module 'studious.lib' has no attribute '{name}'")
    
    @property
    def attach(self):
        from ._attach import attach
        return attach
    
    @property
    def attach2(self):
        from ._attach import attach2
        return attach2
    
    @property
    def Cache(self):
        from ._cache import Cache
        return Cache
    
    @property
    def checksum(self):
        from ._checksum import checksum
        return checksum
    
    @property
    def decrypt(self):
        from ._decrypt import decrypt
        return decrypt
    
    @property
    def df2sql(self):
        from ._df2sql import df2sql
        return df2sql
    
    @property
    def download(self):
        from ._download import download
        return download
    
    @property
    def embd(self):
        from ._embd import embd
        return embd
    
    @property
    def encrypt(self):
        from ._encrypt import encrypt
        return encrypt
    
    @property
    def getkey(self):
        from ._getkey import getkey
        return getkey
    
    @property
    def Random(self):
        from ._random import Random
        return Random
    
    @property
    def scp(self):
        from ._scp import scp
        return scp
    
    @property
    def SQLQuery(self):
        from ._sqlquery import SQLQuery
        return SQLQuery
    
    @property
    def summary(self):
        from ._summary import summary
        return summary
    
    @property
    def Table(self):
        from ._table import Table
        return Table
    
    @property
    def terminal(self):
        from ._terminal import terminal
        return terminal
    
    @property
    def Textarea(self):
        from ._textarea import Textarea
        return Textarea
    
    @property
    def track(self):
        from ._track import track
        return track
    
    @property
    def with_exit_stack(self):
        from ._with_exit_stack import with_exit_stack
        return with_exit_stack
    
__getattr__ = _AutoImport().__getattribute__
