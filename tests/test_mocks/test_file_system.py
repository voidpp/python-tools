import os
import unittest
from copy import copy

from voidpp_tools.mocks.file_system import FileSystem

from voidpp_tools.compat import FileNotFoundError, FileExistsError, UnsupportedOperation

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

    def test_set_data_folder_not_exists(self):
        # Arrange
        fs = FileSystem({})

        # Act & Assert
        with self.assertRaises(FileNotFoundError) as e:
            fs.set_data('/var/lib/filename1', "content1")

    def test_set_data_folder_not_exists_so_create(self):
        # Arrange
        data = {}
        fs = FileSystem(data)

        # Act
        fs.set_data('/var/lib/filename1', "content1", create_folders = True)

        # Assert
        self.assertIn('var', data)
        self.assertIn('lib', data['var'])
        self.assertEqual(fs.get_data('/var/lib/filename1'), "content1")

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

    def test_is_path_exists_with_file(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act & Assert
        with fs.mock():
            self.assertTrue(os.path.exists('filename1'))
            self.assertFalse(os.path.exists('filename2'))

    def test_is_path_exists_with_dir(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act & Assert
        with fs.mock():
            self.assertTrue(os.path.exists('dir1'))
            self.assertFalse(os.path.exists('dir2'))

    def test_is_file_with_file(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act & Assert
        with fs.mock():
            self.assertTrue(os.path.isfile('filename1'))
            self.assertFalse(os.path.isfile('filename2'))

    def test_is_file_with_dir(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act & Assert
        with fs.mock():
            self.assertTrue(os.path.exists('dir1'))
            self.assertFalse(os.path.isfile('dir1'))

    def test_is_dir_with_file(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act & Assert
        with fs.mock():
            self.assertTrue(os.path.isfile('filename1'))
            self.assertFalse(os.path.isdir('filename1'))

    def test_is_dir_with_dir(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act & Assert
        with fs.mock():
            self.assertTrue(os.path.exists('dir1'))
            self.assertFalse(os.path.exists('dir2'))

    def test_file_write(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act
        with fs.mock():
            with open('/dir1/filename3', 'w') as f:
                f.write(u'content 1 to filename 3 in dir1\n')
                f.write(u'content 2 to filename 3 in dir1\n')

        # Assert
        with fs.mock():
            self.assertTrue(os.path.exists('/dir1/filename3'))
            with open('/dir1/filename3') as f:
                self.assertEqual(f.read(), u'content 1 to filename 3 in dir1\ncontent 2 to filename 3 in dir1\n')

    def test_file_write_append(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act
        with fs.mock():
            with open('/dir1/filename4', 'w') as f:
                f.write(u'content 1 to filename 4 in dir1')

            with open('/dir1/filename4', 'a') as f:
                f.write(u'\ncontent 2 to filename 4 in dir1')

        # Assert
        with fs.mock():
            self.assertTrue(os.path.exists('/dir1/filename4'))
            with open('/dir1/filename4') as f:
                self.assertEqual(f.read(), u'content 1 to filename 4 in dir1\ncontent 2 to filename 4 in dir1')

    def test_file_write_dir_not_exists(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act & Assert
        with fs.mock():
            with self.assertRaises(FileNotFoundError):
                open('/dirX/filenameX', 'w')

    def test_file_write_append_not_exists(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act
        with fs.mock():
            with open('/dir1/filenameY', 'a') as f:
                f.write(u'content 1 to filename Y in dir1')

        # Assert
        with fs.mock():
            with open('/dir1/filenameY') as f:
                self.assertTrue(os.path.exists('/dir1/filenameY'))
                self.assertEqual(f.read(), u'content 1 to filename Y in dir1')

    def test_mode_r_not_writable(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act & Assert
        with fs.mock():
            with open('/dir1/dir2/filename2', 'r') as f, self.assertRaises(UnsupportedOperation):
                f.write('test')

    def test_mode_w_not_readable(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act & Assert
        with fs.mock():
            with open('/dir1/filenameZ', 'w') as f, self.assertRaises(UnsupportedOperation):
                f.read()

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

    def test_mkdir(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act & Assert
        with fs.mock():
            os.mkdir('/dir1/dir3')
            self.assertTrue(os.path.exists('/dir1/dir3/'))

    def test_mkdir_existing(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act & Assert
        with fs.mock():
            with self.assertRaises(FileExistsError):
                os.mkdir('/dir1/dir2/')
            self.assertTrue(os.path.exists('/dir1/dir2/filename2'))

    def test_mkdir_in_not_existing_dir(self):
        # Arrange
        data = copy(init_data)
        fs = FileSystem(data)

        # Act & Assert
        with fs.mock():
            with self.assertRaises(FileNotFoundError):
                os.mkdir('/dirX/dir3/')
