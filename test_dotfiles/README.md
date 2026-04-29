# test_dotfiles

`test_dotfiles` contains the smoke test assets for the dotfiles setup flow.

## Files

- `run.sh`: public entrypoint for the Linux Docker smoke test. Builds the test image, runs the smoke test, and saves a log under `test_dotfiles/logs/`.
- `Dockerfile`: container image used by the Linux smoke test.
- `entrypoint.sh`: test driver that prepares an isolated test environment and runs `setup` twice.
- `verify_setup.sh`: post-run assertions for the expected setup output.

## Usage

Run the Linux smoke test from the repository root:

```bash
bash test_dotfiles/run.sh
```

The generated log is written to `test_dotfiles/logs/`.
