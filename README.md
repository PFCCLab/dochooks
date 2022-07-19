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
     rev: v0.2.0
     hooks:
        - id: check-whitespace-between-cn-and-en-char
          files: \.md$|\.rst$
        - id: insert-whitespace-between-cn-and-en-char
          files: \.md$|\.rst$
        - id: api-doc-checker
          files: (?<!index)\.rst$
          additional_dependencies: [".[rst-parser]"]
```
