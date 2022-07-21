VERSION := `poetry run python -c "import sys; from dochooks import __version__ as version; sys.stdout.write(version)"`

test:
  poetry run pytest --workers auto
  just clean

fmt:
  poetry run isort .
  poetry run black .

fmt-docs:
  prettier --write '**/*.md'

lint:
  poetry run pyright dochooks tests

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
