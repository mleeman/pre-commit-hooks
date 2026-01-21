# pre-commit hooks

### Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/mleeman/pre-commit-hooks
    rev: v0.0.1  # Use the ref you want to point at
    hooks:
    -   id: tlv-deb-copyright-year
    # -   id: ...
```

### Hooks available

#### `tlv-deb-copyright-year`
tests if the current year is in the d/copyright file when updating
a repository.

#### `tlv-deb-run-lrc`
run lincensecheck on the package

### Adding a hook
To add a new hook, create the script in `pre_commit_hooks/` and add it to
the `hooks` list in `pre-commit-hooks.yaml`. Add the entry point in the
`setup.cfg` file.

Finally, add a tag with the new version (as listed in `setup.cfg`)
and push to the repository. The tag should be in the format `vX.X.X`
and push it to the remote repository.

Without the tag, the hook will not be available for use.
