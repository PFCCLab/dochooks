# dochooks

Some pre-commit hooks for docs.

<p align="center">
   <a href="LICENSE"><img alt="LICENSE" src="https://img.shields.io/github/license/ShigureLab/dochooks?style=flat-square"></a>
   <a href="https://github.com/psf/black"><img alt="black" src="https://img.shields.io/badge/code%20style-black-000000?style=flat-square"></a>
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
        - id: api-doc-checker
          files: (?<!index)\.rst$
          additional_dependencies: [".[rst-parser]"]
```

## Hooks

### `check-whitespace-between-cn-and-en-char`

用于检查中英文之间是否有空格

### `insert-whitespace-between-cn-and-en-char`

用于自动在中英文之间添加空格

### `api-doc-checker` <sup>WIP</sup>

用于检查 API 文档（reStructureText）格式，需根据规范编写

## TODOs

-  通过 option 的方式设置各个功能的等级，有些实验性功能可以设置为「仅警告」
-  部分 Element 无法获得 lineno
