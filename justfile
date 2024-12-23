VERSION := `uv run python -c "import sys; from dochooks import __version__ as version; sys.stdout.write(version)"`

install:
  uv sync --all-extras --dev

test:
  uv run pytest
  just clean

fmt:
  uv run ruff format .

lint:
  uv run pyright dochooks tests
  uv run ruff check .

fmt-docs:
  prettier --write '**/*.md'

build:
  uv build

release:
  @echo 'Tagging v{{VERSION}}...'
  git tag "v{{VERSION}}"
  @echo 'Push to GitHub to trigger publish process...'
  git push --tags

publish:
  uv build
  uv publish
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
  uv run pre-commit autoupdate

ci-install:
  just install

ci-fmt-check:
  uv run ruff format --check --diff .
  prettier --check '**/*.md'

ci-lint:
  just lint

ci-test:
  uv run pytest --reruns 3 --reruns-delay 1
  just clean
