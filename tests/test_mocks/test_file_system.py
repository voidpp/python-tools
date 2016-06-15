import os
import unittest
from copy import copy

from voidpp_tools.mocks.file_system import FileSystem

from voidpp_tools.compat import FileNotFoundError

init_data = dict(
    filename1 = u"content of filename 1",
    dir1 = dict(
        filename1 = u"content of filename 2 in dir 1",
        dir2 = dict(
            filename2 = u"content of filename 2 in dir 2",
        ),
    ),
)

class TestFileSystem(unittest.TestCase):

    def test_get_data_simple_existing(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act
        result = fs.get_data('filename1')

        # Assert
        self.assertEqual(result, data['filename1'])

    def test_get_data_simple_existing_root(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act
        result = fs.get_data('/filename1')

        # Assert
        self.assertEqual(result, data['filename1'])

    def test_get_data_sub_file(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act
        result = fs.get_data('/dir1/dir2/filename2')

        # Assert
        self.assertEqual(result, data['dir1']['dir2']['filename2'])

    def test_file_open(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act & Assert
        with fs.mock():
            with open('filename1') as f:
                self.assertEqual(f.read(), data['filename1'])

    def test_file_open_not_exists(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act & Assert
        with fs.mock():
            with self.assertRaises(FileNotFoundError):
                open('filename2')

    def test_is_file_exists(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act & Assert
        with fs.mock():
            self.assertEqual(os.path.exists('filename1'), True)

    def test_getcwd(self):
        # Arrange
        fs = FileSystem({}, cwd = '/dir42')

        # Act & Assert
        with fs.mock():
            self.assertEqual(os.getcwd(), '/dir42')

    def test_abspath(self):
        # Arrange
        fs = FileSystem({}, cwd = '/dir1')

        # Act & Assert
        with fs.mock():
            self.assertEqual(os.path.abspath('teve'), '/dir1/teve')
            self.assertEqual(os.path.abspath('/teve'), '/teve')

    def test_expanduser(self):
        # Arrange
        fs = FileSystem({}, user = "douglas")

        # Act & Assert
        with fs.mock():
            self.assertEqual(os.path.expanduser('~/teve'), '/home/douglas/teve')
