from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch

from script.context import Settings
from script.install import npm
from script.installers import install_system_packages
from script.setup_flow import create_dotfile_links


class SetupTests(unittest.TestCase):
    def test_only_tracked_files_are_linked_including_submodules(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root, home, plugin = base / 'repo', base / 'home', base / 'plugin'
            root.mkdir()
            plugin.mkdir()

            def git(directory, *args):
                return subprocess.run(['git', '-C', str(directory), *args], check=True, capture_output=True)

            for directory in (root, plugin):
                git(directory, 'init')
            (plugin / 'init.lua').write_text('-- configuration\n')
            git(plugin, 'add', '.')
            git(plugin, '-c', 'user.name=Test', '-c', 'user.email=test@example.com', 'commit', '-m', 'Initialize')
            git(root, '-c', 'protocol.file.allow=always', 'submodule', 'add', str(plugin), '.config/editor')
            config = root / '.config/tool'
            config.mkdir()
            (config / 'settings.json').write_text('{}')
            (root / '.gitignore').write_text('node_modules/\n*.bak\n')
            git(root, 'add', '.')
            (config / 'node_modules').mkdir()
            (config / 'node_modules/dependency.js').write_text('generated')
            (config / 'settings.json.bak').write_text('backup')
            (config / 'untracked.json').write_text('{}')
            (root / '.config/editor/local-cache').write_text('local')
            settings = Settings(root=root, home=home)
            for _ in range(2):
                create_dotfile_links(settings, Mock())
            self.assertEqual((home / '.config/tool/settings.json').resolve(), config / 'settings.json')
            self.assertTrue((home / '.config/editor/init.lua').is_symlink())
            for path in ('.git', '.gitignore', '.gitmodules', '.config/editor/.git',
                         '.config/editor/local-cache', '.config/tool/node_modules',
                         '.config/tool/settings.json.bak', '.config/tool/untracked.json'):
                self.assertFalse((home / path).exists(), path)

    def test_existing_npm_still_installs_global_packages(self):
        settings = Settings(root=Path.cwd())
        runner = Mock()
        runner.command_exists.return_value = True
        with patch('script.installers.install_npm_global_packages') as install:
            npm.install_tool(settings, runner)
        install.assert_called_once_with(settings, runner)
        runner.run_shell.assert_not_called()

    def test_linux_installs_delta_without_upgrading_system(self):
        runner = Mock()
        settings = Settings(root=Path.cwd(), os_name='linux', ci=False, skip_system_packages=False)
        install_system_packages(settings, runner)
        commands = [call.args[0] for call in runner.run.call_args_list]
        self.assertTrue(any('git-delta' in command for command in commands))
        self.assertFalse(any('upgrade' in command for command in commands))

    def test_macos_installs_delta(self):
        runner = Mock()
        settings = Settings(root=Path.cwd(), os_name='macos', skip_system_packages=False)
        install_system_packages(settings, runner)
        self.assertTrue(any('git-delta' in call.args[0] for call in runner.run.call_args_list))


if __name__ == '__main__':
    unittest.main()
