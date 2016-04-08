
import unittest

from voidpp_tools.mocks.file_system import mockfs
from voidpp_tools.json_config import JSONConfigLoader
from voidpp_tools.config_loader import ConfigLoaderException

class TestConfigLoader(unittest.TestCase):

    @mockfs(dict(etc = {'app1.json': '{"the_answer": 42}'}))
    def test_load_config_from_etc(self):
        # Arrange
        loader = JSONConfigLoader('')

        # Act
        data = loader.load("app1.json")

        # Assert
        self.assertDictEqual(data, dict(the_answer = 42))

    @mockfs()
    def test_load_config_file_not_found(self):
        # Arrange
        loader = JSONConfigLoader('')

        # Act & Assert
        with self.assertRaises(ConfigLoaderException):
            data = loader.load("app1.json")

    @mockfs(dict(
        etc = {'app1.json': '{"the_answer": 42}'},
        home = dict(douglas = {'app1.json': '{"the_question": "6*7"}'})
    ), user = 'douglas')
    def test_load_config_nested(self):
        # Arrange
        loader = JSONConfigLoader('', nested = True)

        # Act
        data = loader.load("app1.json")

        # Assert
        self.assertDictEqual(data, dict(the_answer = 42, the_question = "6*7"))
