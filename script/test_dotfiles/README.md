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

The generated log is written to `script/test_dotfiles/logs/`.
