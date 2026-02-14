# Advanced Git Commands

This guide covers advanced Git commands and their usage, with practical examples for each.

---

## Table of Contents

- [git stash](#git-stash)
- [git cherry-pick](#git-cherry-pick)
- [git revert](#git-revert)
- [git reset](#git-reset)

---

## git stash

`git stash` temporarily saves uncommitted changes (both staged and unstaged) so you can work on something else, then re-apply them later.

### Basic Usage

```bash
# Save current changes to the stash
git stash

# Save with a descriptive message
git stash push -m "work-in-progress: feature login form"
```

### Viewing Stashes

```bash
# List all stashes
git stash list

# Show the contents of the most recent stash
git stash show

# Show the full diff of a stash
git stash show -p stash@{0}
```

### Restoring Stashes

```bash
# Apply the most recent stash and keep it in the stash list
git stash apply

# Apply a specific stash
git stash apply stash@{2}

# Apply the most recent stash and remove it from the stash list
git stash pop
```

### Removing Stashes

```bash
# Drop a specific stash
git stash drop stash@{1}

# Clear all stashes
git stash clear
```

### Example Workflow

```bash
# You're working on a feature but need to fix a bug on main
git stash push -m "feature: half-done sidebar"

git checkout main
# ... fix the bug, commit ...

git checkout feature-branch
git stash pop
# Continue working on the sidebar
```

---

## git cherry-pick

`git cherry-pick` applies the changes from a specific commit onto the current branch. This is useful when you need a particular fix or feature from another branch without merging the entire branch.

### Basic Usage

```bash
# Apply a single commit to the current branch
git cherry-pick <commit-hash>
```

### Options

```bash
# Cherry-pick without automatically committing (stages changes only)
git cherry-pick --no-commit <commit-hash>

# Cherry-pick multiple commits
git cherry-pick <hash1> <hash2> <hash3>

# Cherry-pick a range of commits (exclusive of the first, inclusive of the last)
git cherry-pick <older-hash>..<newer-hash>
```

### Handling Conflicts

```bash
# If a conflict occurs during cherry-pick, resolve it, then:
git add <resolved-files>
git cherry-pick --continue

# Or abort the cherry-pick entirely
git cherry-pick --abort
```

### Example Workflow

```bash
# A critical bugfix was committed on the develop branch
# and you need it on the release branch
git checkout release-branch
git cherry-pick abc1234
# The bugfix commit abc1234 is now applied to release-branch
```

---

## git revert

`git revert` creates a **new commit** that undoes the changes introduced by a previous commit. Unlike `git reset`, it preserves the project history, making it safe to use on shared/public branches.

### Basic Usage

```bash
# Revert a specific commit
git revert <commit-hash>
```

### Options

```bash
# Revert without automatically committing (stages the inverse changes)
git revert --no-commit <commit-hash>

# Revert multiple commits (each gets its own revert commit)
git revert <hash1> <hash2>

# Revert a range of commits
git revert <older-hash>..<newer-hash>
```

### Handling Conflicts

```bash
# If a conflict occurs during revert, resolve it, then:
git add <resolved-files>
git revert --continue

# Or abort the revert
git revert --abort
```

### Example Workflow

```bash
# A commit introduced a bug in production; revert it safely
git log --oneline
# Output:
# f3d9a1b Add experimental caching
# a1b2c3d Update API endpoint
# ...

git revert f3d9a1b
# Creates a new commit that undoes the changes from f3d9a1b
# History is preserved — the original commit and the revert are both visible
```

---

## git reset

`git reset` moves the current branch pointer to a specified commit, optionally modifying the staging area and working directory. It is typically used to undo local changes that have **not** been pushed.

> **Caution:** `git reset --hard` permanently discards changes. Use it carefully, especially on shared branches.

### Three Modes

| Mode      | Branch Pointer | Staging Area | Working Directory |
|-----------|:--------------:|:------------:|:-----------------:|
| `--soft`  | Moved          | Unchanged    | Unchanged         |
| `--mixed` | Moved          | Reset        | Unchanged         |
| `--hard`  | Moved          | Reset        | Reset             |

### Basic Usage

```bash
# Soft reset — keep changes staged
git reset --soft <commit-hash>

# Mixed reset (default) — unstage changes but keep them in working directory
git reset --mixed <commit-hash>
# or simply:
git reset <commit-hash>

# Hard reset — discard all changes
git reset --hard <commit-hash>
```

### Common Patterns

```bash
# Undo the last commit but keep the changes staged
git reset --soft HEAD~1

# Undo the last commit and unstage the changes
git reset HEAD~1

# Completely discard the last 3 commits and all their changes
git reset --hard HEAD~3

# Unstage a specific file
git reset HEAD <file>
```

### Example Workflow

```bash
# You made a commit with a typo in the message and haven't pushed yet
git reset --soft HEAD~1
# Changes are still staged; fix anything you need, then recommit
git commit -m "Corrected commit message"
```

---

## Quick Reference

| Command            | Creates New Commit? | Safe for Shared Branches? | Primary Use Case                        |
|--------------------|:-------------------:|:-------------------------:|-----------------------------------------|
| `git stash`        | No                  | N/A                       | Temporarily shelve uncommitted changes  |
| `git cherry-pick`  | Yes                 | Yes                       | Copy specific commits to another branch |
| `git revert`       | Yes                 | Yes                       | Undo a commit while preserving history  |
| `git reset`        | No                  | No (if pushed)            | Undo local commits or unstage changes   |
