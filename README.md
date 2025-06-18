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
tests if the current year is in the d/copyright file when updating a repository.

#### `tlv-deb-run-lrc`
run lincensecheck on the package
