"""

"""

from __future__ import annotations
from ._auto import auto
from ._config import config
from ._version import __version__
from . import lib
from . import app


auto.warnings.filterwarnings(
    "ignore",
    category = UserWarning,
    message = '.*pandas only supports SQLAlchemy connectable.*',
)
