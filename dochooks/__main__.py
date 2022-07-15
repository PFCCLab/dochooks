import argparse

from dochooks import __version__


def main() -> None:
    parser = argparse.ArgumentParser(prog="dochooks", description="pre-commit hooks")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = parser.parse_args()  # type: ignore


if __name__ == "__main__":
    main()
