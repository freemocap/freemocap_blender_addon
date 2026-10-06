import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from tools import run_tests, test_blender_package


class RunnerTests(unittest.TestCase):
    def test_zero_process_exit_without_test_completion_is_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(test_blender_package.subprocess, 'run', return_value=SimpleNamespace(returncode=0)):
                with self.assertRaisesRegex(RuntimeError, 'without completing checks'):
                    test_blender_package.run(Path('unused-blender'), 'legacy', Path('unused.zip'), output=Path(directory))

    def test_blender_cannot_inherit_callers_python_dependency_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict('os.environ', PYTHONPATH='foreign packages', PYTHONHOME='foreign python'):
                environment = test_blender_package.isolated_environment(Path(directory))
            self.assertNotIn('PYTHONPATH', environment)
            self.assertNotIn('PYTHONHOME', environment)
            self.assertEqual(environment['PYTHONNOUSERSITE'], '1')

    def test_launcher_ini_custom_library_and_escaped_windows_separators(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            settings = root / 'Blender Launcher'
            settings.mkdir()
            (settings / 'Blender Launcher.ini').write_text('[General]\nlibrary_folder=C:\\\\Builds\\\\Blender\n')
            with patch.dict('os.environ', LOCALAPPDATA=directory):
                self.assertEqual(str(run_tests.launcher_library()), str(Path('C:\\Builds\\Blender')))

    def test_discovery_ignores_download_staging_and_forks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for folder in ('stable/blender-a', 'daily/blender-b', '.temp/incomplete', 'bforartists/fork'):
                path = root / folder / 'blender.exe'
                path.parent.mkdir(parents=True)
                path.touch()
            self.assertEqual(run_tests.discover(root), sorted([
                (root / 'stable/blender-a/blender.exe').resolve(),
                (root / 'daily/blender-b/blender.exe').resolve()]))

    def test_formats_selected_from_actual_blender_version(self):
        old = dict(blender=[3, 0, 1], python='3.9', system='Windows', machine='AMD64')
        self.assertEqual(run_tests.target(old), ('windows-x64', ['legacy']))
        modern = dict(old, blender=[5, 2, 2], python='3.13')
        self.assertEqual(run_tests.target(modern), ('windows-x64', ['legacy', 'extension']))
        with self.assertRaises(ValueError):
            run_tests.target(dict(old, machine='unknown'))

    def test_failed_build_is_visible_in_json_and_junit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run_tests.write_reports(root, [dict(name='bad build', status='failed', error='missing wheel', seconds=0)])
            self.assertEqual(json.loads((root / 'summary.json').read_text())[0]['status'], 'failed')
            suite = ET.parse(root / 'junit.xml').getroot()
            self.assertEqual(suite.attrib['failures'], '1')
            self.assertEqual(suite.find('testcase/failure').attrib['message'], 'missing wheel')


if __name__ == '__main__':
    unittest.main()
