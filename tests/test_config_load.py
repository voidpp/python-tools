
import pytest

from voidpp_tools.mocks.file_system import mockfs
from voidpp_tools.json_config import JSONConfigLoader
from voidpp_tools.config_loader import ConfigFileNotFoundException

@mockfs(dict(etc = {'app1.json': u'{"the_answer": 42}'}))
def test_load_config_from_etc():
    # Arrange
    loader = JSONConfigLoader('')

    # Act
    data = loader.load("app1.json")

    # Assert
    assert data == dict(the_answer = 42)

@mockfs()
def test_load_config_file_not_found():
    # Arrange
    loader = JSONConfigLoader('')

    # Act & Assert
    with pytest.raises(ConfigFileNotFoundException):
        loader.load("app1.json")

@mockfs(dict(
    etc = {'app1.json': u'{"the_answer": 42}'},
    home = dict(douglas = {'app1.json': u'{"the_question": "6*7"}'})
), user = 'douglas')
def test_load_config_nested():
    # Arrange
    loader = JSONConfigLoader('', nested = True)

    # Act
    data = loader.load("app1.json")

    # Assert
    assert data == dict(the_answer = 42, the_question = "6*7")
