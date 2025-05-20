# Git Hooks Cheat Sheet

Reassigning the location of hooks:

```shell
git config --global core.hooksPath ./.githooks
```

Prints all git global settings to the console,
after changing the location of git hooks,
in the settings `core.hookspath=./.githooks` appears:

```shell
git config --global --list
```

Returns the default value of the `core.hookspath` config:

```shell
git config --global --unset core.hooksPath
```

## Pull

1. post-merge

## Fetch

-

## Merge

1. post-index-change
2. post-merge

## Add

1. post-index-change

## Commit

1. post-index-change
2. pre-commit
3. prepare-commit-msg
4. commit-msg
5. post-commit

## Push

1. pre-push
