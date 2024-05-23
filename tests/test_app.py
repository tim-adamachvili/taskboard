import pytest
from app import TaskBoardApp


@pytest.fixture(scope='module')
def app():
    app = TaskBoardApp(memory=True)
    app.app.config['TESTING'] = True
    app.Base.metadata.create_all(app.engine)

    yield app

    app.Base.metadata.drop_all(app.engine)


@pytest.fixture(scope='module')
def client(app):
    with app.app.test_client() as client:
        with app.app.app_context():
            yield client


@pytest.fixture
def db_session(app):
    connection = app.engine.connect()
    transaction = connection.begin()
    session = app.Session(bind=connection)
    app.session = session

    yield session

    session.close()
    transaction.rollback()
    connection.close()


def test_get_lists(app, client, db_session):
    client.post('/lists', json={'name': 'Test List'})
    response = client.get('/lists')
    assert response.status_code == 200

    # Directly query the in-memory database
    lists = db_session.query(app.List).all()
    assert len(lists) == 1
    assert lists[0].name == 'Test List'


def test_create_task(app, client, db_session):
    list_response = client.post('/lists', json={'name': 'Test List'})
    list_id = list_response.get_json()['id']
    response = client.post(f'/lists/{list_id}/tasks', json={'name': 'Test Task', 'description': 'This is a test task'})
    assert response.status_code == 201

    new_task = db_session.query(app.Task).filter_by(name='Test Task').one_or_none()
    assert new_task is not None
    assert new_task.name == 'Test Task'
    assert new_task.description == 'This is a test task'


def test_update_task(app, client, db_session):
    list_response = client.post('/lists', json={'name': 'Test List'})
    list_id = list_response.get_json()['id']
    task_response = client.post(f'/lists/{list_id}/tasks', json={'name': 'Test Task', 'description': 'This is a test task'})
    task_id = task_response.get_json()['id']

    response = client.put(f'/tasks/{task_id}', json={'name': 'Updated Task', 'description': 'Updated description'})
    assert response.status_code == 200

    updated_task = db_session.query(app.Task).filter_by(id=task_id).one_or_none()
    assert updated_task is not None
    assert updated_task.name == 'Updated Task'
    assert updated_task.description == 'Updated description'


def test_delete_task(app, client, db_session):
    list_response = client.post('/lists', json={'name': 'Test List'})
    list_id = list_response.get_json()['id']
    task_response = client.post(f'/lists/{list_id}/tasks', json={'name': 'Test Task', 'description': 'This is a test task'})
    task_id = task_response.get_json()['id']

    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 204

    deleted_task = db_session.query(app.Task).filter_by(id=task_id).one_or_none()
    assert deleted_task is None


def test_delete_list(app, client, db_session):
    list_response = client.post('/lists', json={'name': 'Test List'})
    list_id = list_response.get_json()['id']
    response = client.delete(f'/lists/{list_id}')
    assert response.status_code == 204

    deleted_list = db_session.query(app.List).filter_by(id=list_id).one_or_none()
    assert deleted_list is None


def test_move_task(app, client, db_session):
    list_response1 = client.post('/lists', json={'name': 'Test List 1'})
    list_id1 = list_response1.get_json()['id']
    list_response2 = client.post('/lists', json={'name': 'Test List 2'})
    list_id2 = list_response2.get_json()['id']

    task_response = client.post(f'/lists/{list_id1}/tasks', json={'name': 'Test Task', 'description': 'This is a test task'})
    task_id = task_response.get_json()['id']

    response = client.put(f'/tasks/{task_id}/move', json={'list_id': list_id2})
    assert response.status_code == 200

    moved_task = db_session.query(app.Task).filter_by(id=task_id).one_or_none()
    assert moved_task is not None
    assert moved_task.list_id == list_id2
