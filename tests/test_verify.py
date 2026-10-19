from pathlib import Path
import tempfile
import unittest

from script.test_dotfiles.verify import _assert_symlink_target


class SymlinkVerificationTests(unittest.TestCase):
    def test_directory_aliases_identify_the_same_target(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            real = base / 'private-tmp'
            real.mkdir()
            alias = base / 'tmp'
            alias.symlink_to(real, target_is_directory=True)
            target = real / '.tmux.conf'
            target.write_text('configuration')
            link = base / 'installed-config'
            link.symlink_to(target.resolve())
            _assert_symlink_target(link, alias / '.tmux.conf')

    def test_wrong_target_and_regular_file_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            expected, other = base / 'expected', base / 'other'
            expected.write_text('same content')
            other.write_text('same content')
            link = base / 'installed-config'
            link.symlink_to(other)
            with self.assertRaisesRegex(RuntimeError, 'Unexpected symlink target'):
                _assert_symlink_target(link, expected)
            with self.assertRaisesRegex(RuntimeError, 'Expected symlink'):
                _assert_symlink_target(expected, expected)
