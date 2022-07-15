import toml

from pre_commit_hooks import __version__

with open("pyproject.toml", "r") as f:
    project_info = toml.load(f)


def test_version():
    assert __version__ == project_info["tool"]["poetry"]["version"]
