import contextlib
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from script.util import CommandRunner
from script.test_dotfiles.runner import run_smoke_test


class GitHubAuthenticationTests(unittest.TestCase):
    def test_only_github_api_receives_authentication(self):
        for url, authenticated in (
            ('https://api.github.com/repos/neovim/neovim/releases/latest', True),
            ('https://example.com/data', False),
            ('https://api.github.com.example.com/data', False),
            ('http://api.github.com/data', False),
        ):
            with self.subTest(url=url), patch.dict(os.environ, {'GITHUB_TOKEN': 'test-token'}, clear=True):
                with patch('script.util.urllib.request.urlopen') as open_url:
                    open_url.return_value.__enter__.return_value = io.StringIO('{}')
                    self.assertEqual(CommandRunner().fetch_json(url), {})
                    header = open_url.call_args.args[0].get_header('Authorization')
                    self.assertEqual(header, 'Bearer test-token' if authenticated else None)

    def test_optional_token_and_gh_token_fallback(self):
        for env, expected in (({}, None), ({'GH_TOKEN': 'fallback'}, 'Bearer fallback')):
            with patch.dict(os.environ, env, clear=True), patch('script.util.urllib.request.urlopen') as open_url:
                open_url.return_value.__enter__.return_value = io.StringIO('{}')
                CommandRunner().fetch_json('https://api.github.com/repos/neovim/neovim/releases/latest')
                self.assertEqual(open_url.call_args.args[0].get_header('Authorization'), expected)

    def test_docker_forwards_token_names_without_logging_values(self):
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'script/test_dotfiles').mkdir(parents=True)
            with patch.dict(os.environ, {'GITHUB_TOKEN': 'secret-github', 'GH_TOKEN': 'secret-gh'}, clear=True):
                with patch('script.test_dotfiles.runner._stream_command') as command:
                    with contextlib.redirect_stdout(output):
                        self.assertEqual(run_smoke_test(root, interactive=False), 0)
                    docker_args = command.call_args.args[0]
                    self.assertIn('GITHUB_TOKEN', docker_args)
                    self.assertIn('GH_TOKEN', docker_args)
                    for secret in ('secret-github', 'secret-gh'):
                        self.assertNotIn(secret, ' '.join(docker_args))
                        self.assertNotIn(secret, output.getvalue())
                        for log in (root / 'script/test_dotfiles/logs').iterdir():
                            self.assertNotIn(secret, log.read_text())
