# Documenting urdf2mjcf

## Changelog generation

### Requirements

```shell
pip install "git-changelog==2.1.0"
```

### Generating the changelog

```shell
cd path/to/urdf2mjcf
git-changelog -c conventional -t angular -s "feat,refactor,fix,revert,docs,deps,style,build,test,ci,chore" -r . > CHANGELOG.md 
```
