# script.test_dotfiles

`script/test_dotfiles` contains the Linux smoke test assets for the dotfiles setup flow.

## Files

- `runner.py`: builds the Docker image, runs the smoke test, and stores logs under `script/test_dotfiles/logs/`.
- `entrypoint.py`: test driver executed inside the Docker container.
- `verify.py`: post-run assertions for the expected setup output.
- `Dockerfile`: container image used by the Linux smoke test.

## Usage

Run the smoke test from the repository root:

```bash
uv run python script/dotfiles.py test
```

When a TTY is available, this opens a shell in the same container after the smoke test passes. In non-TTY environments it automatically falls back to non-interactive mode and writes the generated log to `script/test_dotfiles/logs/`.

To force non-interactive mode, run:

```bash
uv run python script/dotfiles.py test --no-interactive
```

In interactive mode, exit the shell to end the test run.
