"""

"""

from __future__ import annotations
from .._auto import auto


def Random(*seeds: int) -> _Random:
    assert len(seeds) > 0, len(seeds)
    seed = auto.json.dumps(seeds, separators=(',', ':'))
    seed = auto.hashlib.md5(seed.encode()).digest()

    random = auto.random.Random(seed)

    return random
