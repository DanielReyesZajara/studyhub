def test_empty_list(client):
    response = client.get('/api/tasks')
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_task(client):
    response = client.post('/api/tasks', json={'title': 'Repasar Docker'})
    assert response.status_code == 201
    assert response.get_json()['completed'] is False
