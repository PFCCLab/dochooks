# dochooks

Some pre-commit hooks for docs.

<p align="center">
   <a href="LICENSE"><img alt="LICENSE" src="https://img.shields.io/github/license/ShigureLab/dochooks?style=flat-square"></a>
   <a href="https://github.com/astral-sh/ruff"><img alt="ruff" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square"></a>
   <a href="https://gitmoji.dev"><img src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67?style=flat-square" alt="Gitmoji"></a>
</p>

## Usage

`.pre-commit-config.yaml`

```yaml
repos:
   - repo: https://github.com/ShigureLab/dochooks
     rev: v0.3.0
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
