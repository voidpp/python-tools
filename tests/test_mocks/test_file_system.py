import os
from copy import copy
import pytest

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

def test_set_data_folder_not_exists():
    # Arrange
    fs = FileSystem({})

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        fs.set_data('/var/lib/filename1', "content1")

def test_set_data_folder_not_exists_so_create():
    # Arrange
    data = {}
    fs = FileSystem(data)

    # Act
    fs.set_data('/var/lib/filename1', "content1", create_folders = True)

    # Assert
    assert 'var' in data
    assert 'lib' in data['var']
    assert fs.get_data('/var/lib/filename1') == "content1"

def test_get_data_simple_existing():
    # Arrange
    data = copy(init_data)
    fs = FileSystem(data)

    # Act
    result = fs.get_data('filename1')

    # Assert
    assert result == data['filename1']

def test_get_data_simple_existing_root():
    # Arrange
    data = copy(init_data)
    fs = FileSystem(data)

    # Act
    result = fs.get_data('/filename1')

    # Assert
    assert result == data['filename1']

def test_get_data_sub_file():
    # Arrange
    data = copy(init_data)
    fs = FileSystem(data)

    # Act
    result = fs.get_data('/dir1/dir2/filename2')

    # Assert
    assert result == data['dir1']['dir2']['filename2']

def test_file_open():
    # Arrange
    data = copy(init_data)
    fs = FileSystem(data)

    # Act & Assert
    with fs.mock():
        with open('filename1') as f:
            assert f.read() == data['filename1']

def test_file_open_not_exists():
    # Arrange
    data = copy(init_data)
    fs = FileSystem(data)

    # Act & Assert
    with fs.mock():
        with pytest.raises(FileNotFoundError):
            open('filename2')

def test_is_path_exists_with_file():
    # Arrange
    data = copy(init_data)
    fs = FileSystem(data)

    # Act & Assert
    with fs.mock():
        assert os.path.exists('filename1')
        assert not os.path.exists('filename2')

def test_is_path_exists_with_dir():
    # Arrange
    data = copy(init_data)
    fs = FileSystem(data)

    # Act & Assert
    with fs.mock():
        assert os.path.exists('dir1')
        assert not os.path.exists('dir2')

def test_is_file_with_file():
    # Arrange
    data = copy(init_data)
    fs = FileSystem(data)

    # Act & Assert
    with fs.mock():
        assert os.path.isfile('filename1')
        assert not os.path.isfile('filename2')

def test_is_file_with_dir():
    # Arrange
    data = copy(init_data)
    fs = FileSystem(data)

    # Act & Assert
    with fs.mock():
        assert os.path.exists('dir1')
        assert not os.path.isfile('dir1')

def test_is_dir_with_file():
    # Arrange
    data = copy(init_data)
    fs = FileSystem(data)

    # Act & Assert
    with fs.mock():
        assert os.path.isfile('filename1')
        assert not os.path.isdir('filename1')

def test_is_dir_with_dir():
    # Arrange
    data = copy(init_data)
    fs = FileSystem(data)

    # Act & Assert
    with fs.mock():
        assert os.path.exists('dir1')
        assert not os.path.exists('dir2')

def test_file_write():
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
        assert os.path.exists('/dir1/filename3')
        with open('/dir1/filename3') as f:
            assert f.read() == u'content 1 to filename 3 in dir1\ncontent 2 to filename 3 in dir1\n'

def test_file_write_append():
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
        assert os.path.exists('/dir1/filename4')
        with open('/dir1/filename4') as f:
            assert f.read() == u'content 1 to filename 4 in dir1\ncontent 2 to filename 4 in dir1'

def test_file_write_dir_not_exists():
    # Arrange
    data = copy(init_data)
    fs = FileSystem(data)

    # Act & Assert
    with fs.mock():
        with pytest.raises(FileNotFoundError):
            open('/dirX/filenameX', 'w')

def test_file_write_append_not_exists():
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
            assert os.path.exists('/dir1/filenameY')
            assert f.read() == u'content 1 to filename Y in dir1'

def test_mode_r_not_writable():
    # Arrange
    data = copy(init_data)
    fs = FileSystem(data)

    # Act & Assert
    with fs.mock():
        with open('/dir1/dir2/filename2', 'r') as f, pytest.raises(UnsupportedOperation):
            f.write('test')

def test_mode_w_not_readable():
    # Arrange
    data = copy(init_data)
    fs = FileSystem(data)

    # Act & Assert
    with fs.mock():
        with open('/dir1/filenameZ', 'w') as f, pytest.raises(UnsupportedOperation):
            f.read()

def test_getcwd():
    # Arrange
    fs = FileSystem({}, cwd = '/dir42')

    # Act & Assert
    with fs.mock():
        assert os.getcwd() == '/dir42'

def test_abspath():
    # Arrange
    fs = FileSystem({}, cwd = '/dir1')

    # Act & Assert
    with fs.mock():
        assert os.path.abspath('teve') == '/dir1/teve'
        assert os.path.abspath('/teve') == '/teve'

def test_expanduser():
    # Arrange
    fs = FileSystem({}, user = "douglas")

    # Act & Assert
    with fs.mock():
        assert os.path.expanduser('~/teve') == '/home/douglas/teve'

def test_mkdir():
    # Arrange
    data = copy(init_data)
    fs = FileSystem(data)

    # Act & Assert
    with fs.mock():
        os.mkdir('/dir1/dir3')
        assert os.path.exists('/dir1/dir3/')

def test_mkdir_existing():
    # Arrange
    data = copy(init_data)
    fs = FileSystem(data)

    # Act & Assert
    with fs.mock():
        with pytest.raises(FileExistsError):
            os.mkdir('/dir1/dir2/')
        assert os.path.exists('/dir1/dir2/filename2')

def test_mkdir_in_not_existing_dir():
    # Arrange
    data = copy(init_data)
    fs = FileSystem(data)

    # Act & Assert
    with fs.mock():
        with pytest.raises(FileNotFoundError):
            os.mkdir('/dirX/dir3/')

def test_chmod():
    # Arrange
    fs = FileSystem({})

    with fs.mock():
        os.chmod('/noooo/fff.txt', 42)

def test_stat():
    # Arrange
    fs = FileSystem({})

    with fs.mock():
        os.stat('/noooo/fff.txt')
