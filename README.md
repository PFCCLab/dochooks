# dochooks

Some pre-commit hooks for docs.

<p align="center">
   <a href="https://python.org/" target="_blank"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/dochooks?logo=python&style=flat-square"></a>
   <a href="https://pypi.org/project/dochooks/" target="_blank"><img src="https://img.shields.io/pypi/v/dochooks?style=flat-square" alt="pypi"></a>
   <a href="https://pypi.org/project/dochooks/" target="_blank"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/dochooks?style=flat-square"></a>
   <a href="LICENSE"><img alt="LICENSE" src="https://img.shields.io/github/license/PFCCLab/dochooks?style=flat-square"></a>
   <br/>
   <a href="https://github.com/astral-sh/uv"><img alt="uv" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json&style=flat-square"></a>
   <a href="https://github.com/astral-sh/ruff"><img alt="ruff" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square"></a>
   <a href="https://gitmoji.dev"><img alt="Gitmoji" src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67?style=flat-square"></a>
</p>

## Usage

`.pre-commit-config.yaml`

```yaml
repos:
   - repo: https://github.com/PFCCLab/dochooks
     rev: v0.5.0
     hooks:
        - id: check-whitespace-between-cn-and-en-char
          files: \.md$|\.rst$
        - id: insert-whitespace-between-cn-and-en-char
          files: \.md$|\.rst$
```

## Hooks

### `check-whitespace-between-cn-and-en-char`

用于检查中英文之间是否有空格

### `insert-whitespace-between-cn-and-en-char`

用于自动在中英文之间添加空格

## Pragma

dochooks 支持 `dochooks: skip-next-line` 和 `dochooks: skip-line` 两种 pragma

<!-- prettier-ignore -->
```markdown
<!-- dochooks: skip-next-line -->
这是一段中文and English混合的text
这是一段中文and English混合的text  <!-- dochooks: skip-line -->
```
