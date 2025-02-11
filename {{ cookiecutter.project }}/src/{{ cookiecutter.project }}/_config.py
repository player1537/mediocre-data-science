"""

"""

from __future__ import annotations
from ._auto import auto


auto.dotenv.load_dotenv()


config = auto.types.SimpleNamespace()

config.rootdir = auto.pathlib.Path(auto.os.environ['{{ cookiecutter.PROJECT }}_ROOTDIR'])
assert config.rootdir.exists(), config.rootdir

config.datadir = auto.pathlib.Path(auto.os.environ.get(
    '{{ cookiecutter.PROJECT }}_DATADIR',
    config.rootdir / 'data',
))
assert config.datadir.exists(), config.datadir

config.tempdir = auto.pathlib.Path(auto.os.environ.get(
    '{{ cookiecutter.PROJECT }}_TEMPDIR',
    config.rootdir / 'temp',
))
assert config.tempdir.exists(), config.tempdir


config.a = auto.types.SimpleNamespace()

config.a.datadir = config.datadir / 'a'
config.a.datadir.mkdir(exist_ok = True)
assert config.a.datadir.exists(), config.a.datadir
