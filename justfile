VERSION := `poetry run python -c "import sys; from dochooks import __version__ as version; sys.stdout.write(version)"`

install:
  poetry install -E rst-parser

test:
  poetry run pytest
  just clean

fmt:
  poetry run ruff format .

lint:
  poetry run pyright dochooks tests
  poetry run ruff check .

fmt-docs:
  prettier --write '**/*.md'

build:
  poetry build

publish:
  touch dochooks/py.typed
  poetry publish --build
  git tag "v{{VERSION}}"
  git push --tags
  just clean-builds

clean:
  find . -name "*.pyc" -print0 | xargs -0 rm -f
  rm -rf .pytest_cache/
  rm -rf .mypy_cache/
  find . -maxdepth 3 -type d -empty -print0 | xargs -0 -r rm -r

clean-builds:
  rm -rf build/
  rm -rf dist/
  rm -rf *.egg-info/

hooks-update:
  poetry run pre-commit autoupdate

ci-install:
  poetry install --no-interaction --no-root -E rst-parser

ci-fmt-check:
  poetry run ruff format --check --diff .
  prettier --check '**/*.md'

ci-lint:
  just lint

ci-test:
  poetry run pytest --reruns 3 --reruns-delay 1
  just clean
