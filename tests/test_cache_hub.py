import json
from voidpp_tools.mocks.file_system import FileSystem, mockfs
from voidpp_tools.cache import FileCacheHub

def test_create_cache_file():

    fs = FileSystem({})

    with fs.mock():
        hub = FileCacheHub('/teve.json', 0)
        hub.flush()

    assert fs.get_data('/teve.json') == '{}'


@mockfs()
def test_get_default_value_root():

    hub = FileCacheHub('/teve.json', 0)

    data = hub.get_node_data(default = [])

    assert data == []


@mockfs()
def test_get_default_value_sub_node():

    hub = FileCacheHub('/teve.json', 0)

    data = hub.get_node_data('path', default = [])

    assert data == []


@mockfs()
def test_get_default_value_very_sub_node():

    hub = FileCacheHub('/teve.json', 0)

    data = hub.get_node_data('path1.path2.path3', default = [])

    assert data == []


@mockfs({'teve.json': '[2,4,6]'})
def test_get_value_root():

    hub = FileCacheHub('/teve.json', 0)

    data = hub.get_node_data(default = [])

    assert data == [2,4,6]


@mockfs({'teve.json': '{"path1": [5,10]}'})
def test_get_value_sub_node():

    hub = FileCacheHub('/teve.json', 0)

    data = hub.get_node_data('path1', default = [])

    assert data == [5,10]


@mockfs({'teve.json': '{"path1": {"path2": [4,8]}}'})
def test_get_value_very_sub_node():

    hub = FileCacheHub('/teve.json', 0)

    data = hub.get_node_data('path1.path2', default = [])

    assert data == [4,8]


def test_set_value_root():

    fs = FileSystem({})

    with fs.mock():
        hub = FileCacheHub('/teve.json', 0)
        hub.save_node_data('', [2,4,5])

    assert json.loads(fs.get_data('/teve.json')) == [2,4,5]


def test_update_value_root():

    fs = FileSystem({'teve.json': '[1,5,10]'})

    with fs.mock():
        hub = FileCacheHub('/teve.json', 0)
        hub.save_node_data('', [2,4])

    assert json.loads(fs.get_data('/teve.json')) == [2,4]


def test_update_value_very_sub_node():

    fs = FileSystem({'teve.json': '{"path1": {"path2": [4,8]}}'})

    with fs.mock():
        hub = FileCacheHub('/teve.json', 0)
        hub.save_node_data('path1.path2', [2,4])

    assert json.loads(fs.get_data('/teve.json')) == {'path1':{'path2':[2,4]}}
