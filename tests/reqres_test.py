import json

import requests
from jsonschema.validators import validate


def test_list_users(base_url):
    response = requests.get(base_url + '/api/users', params='page=2')
    assert response.status_code == 200
    assert response.json()['page'] == 2
    assert response.json()['data'] != []


def test_single_user(base_url):
    id = 2
    email = 'janet.weaver@reqres.in'
    first_name = 'Janet'
    last_name = 'Weaver'
    response = requests.get(base_url + '/api/users/2')
    assert response.status_code == 200
    assert response.json()['data']['id'] == id
    assert response.json()['data']['email'] == email
    assert response.json()['data']['first_name'] == first_name
    assert response.json()['data']['last_name'] == last_name


def test_single_user_not_found(base_url):
    response = requests.get(base_url + '/api/users/23')
    assert response.status_code == 404


def test_list_resource(base_url):
    text = 'To keep ReqRes free, contributions towards server costs are appreciated!'
    response = requests.get(base_url + '/api/unknown')
    assert response.status_code == 200
    assert response.json()['data'] != []
    assert response.json()['total'] == 12
    assert response.json()['support']['text'] == text


def test_single_resource(base_url):
    data = {
        "id": 2,
        "name": "fuchsia rose",
        "year": 2001,
        "color": "#C74375",
        "pantone_value": "17-2031"
    }
    response = requests.get(base_url + '/api/unknown/2')
    assert response.status_code == 200
    assert response.json()['data'] == data


def test_single_resource_not_found(base_url):
    response = requests.get(base_url + '/api/unknown/23')
    assert response.status_code == 404


def test_login_successful(base_url):
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }
    response = requests.post(base_url + '/api/login', data=payload)
    assert response.status_code == 200
    assert 'token' in response.json()
    assert response.json()['token']


def test_login_unsuccessful(base_url):
    payload = {
        "email": "peter@klaven"
    }
    error = 'Missing password'
    response = requests.post(base_url + '/api/login', data=payload)
    assert response.status_code == 400
    assert response.json()['error'] == error


def test_register_successful(base_url):
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }
    response = requests.post(base_url + '/api/register', data=payload)
    assert response.status_code == 200
    assert response.json()['id'] == 4
    assert response.json()['token']


def test_register_unsuccessful(base_url):
    payload = {
        "email": "sydney@fife"
    }
    error = 'Missing password'
    response = requests.post(base_url + '/api/register', data=payload)
    assert response.status_code == 400
    assert response.json()['error'] == error


def test_create(base_url):
    payload = {
        "name": "morpheus",
        "job": "leader"
    }
    name = 'morpheus'
    job = 'leader'
    response = requests.post(base_url + '/api/users', data=payload)
    assert response.status_code == 201
    assert response.json()['name'] == name
    assert response.json()['job'] == job
    assert response.json()['id']


def test_delete(base_url):
    payload = {
        "name": "morpheus",
        "job": "leader"
    }
    response = requests.post(base_url + '/api/users', data=payload)
    id = response.json()['id']
    delete = requests.delete(base_url + '/api/users/' + id)
    assert delete.status_code == 204


def test_update(base_url):
    payload_post = {
        "name": "morpheus",
        "job": "leader"
    }
    payload_update = {
        "name": "morpheus",
        "job": "zion resident"
    }
    new_job = 'zion resident'
    response = requests.post(base_url + '/api/users', data=payload_post)
    id = response.json()['id']
    update = requests.put(base_url + '/api/users/' + id, data=payload_update)
    assert update.status_code == 200
    assert update.json()['job'] == new_job


def test_patch(base_url):
    payload_post = {
        "name": "morpheus",
        "job": "leader"
    }
    payload_update = {
        "name": "morpheus",
        "job": "zion resident"
    }
    new_job = 'zion resident'
    response = requests.post(base_url + '/api/users', data=payload_post)
    id = response.json()['id']
    update = requests.patch(base_url + '/api/users/' + id, data=payload_update)
    assert update.status_code == 200
    assert update.json()['job'] == new_job


def test_list_users_schema(base_url):
    response = requests.get(base_url + '/api/users', params='page=2')
    assert response.status_code == 200
    # Валидация ответа от сервера
    with open('../schemas/list_user.json') as file:
        schema = json.load(file)
    validate(instance=response.json(), schema=schema)


def test_single_user_schema(base_url):
    response = requests.get(base_url + '/api/users/2')
    assert response.status_code == 200
    with open('../schemas/single_user.json') as file:
        schema = json.load(file)
    validate(instance=response.json(), schema=schema)


def test_list_resource_schema(base_url):
    response = requests.get(base_url + '/api/unknown')
    assert response.status_code == 200
    with open('../schemas/list_resources.json') as file:
        schema = json.load(file)
    validate(instance=response.json(), schema=schema)


def test_single_resource_schema(base_url):
    response = requests.get(base_url + '/api/unknown/2')
    assert response.status_code == 200
    with open('../schemas/single_resources.json') as file:
        schema = json.load(file)
    validate(instance=response.json(), schema=schema)


def test_login_successful_schema(base_url):
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }
    response = requests.post(base_url + '/api/login', data=payload)
    assert response.status_code == 200
    with open('../schemas/login_successful.json') as file:
        schema = json.load(file)
    validate(instance=response.json(), schema=schema)
