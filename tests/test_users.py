from http import HTTPStatus

import pytest

from users.schemas import UserCreateOutput

@pytest.mark.asyncio
async def test_create_user(client):

    response = await client.post(
        '/users/create',
        json={
            'username': 'test',
            'email': 'test@test.com',
            'password': '@Ter1234',
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['id'] == 1

@pytest.mark.asyncio
async def test_create_user_exception_username_exists(client, user):

    response = await client.post(
        '/users/create',
        json={
            'username': user.username,
            'email': 'test@test.com',
            'password': '@Test1234',
        }
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_create_user_exception_email_exists(client, user):

    response = await client.post(
        '/users/create',
        json={
            'username': 'test',
            'email': user.email,
            'password': '@Test1234',
        }
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_read_users(client):
    response = await client.get('/users/list')

    assert response.status_code == HTTPStatus.OK
    print(response.json())
    assert response.json() == []



@pytest.mark.asyncio
async def test_read_users_with_user(client, user):
    user_schema = UserCreateOutput.model_validate(user).model_dump()
    response = await client.get('/users/list')

    assert response.status_code == HTTPStatus.OK
    assert response.json() ==  [user_schema]



@pytest.mark.asyncio
async def test_update_user(client, user, token):

    response = await client.put(
        f'/users/update/{user.id}',
        headers={'authorization': f'Bearer {token}'},
        json={
            'username': 'test2',
            'email': 'test@test.com',
        }
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'test2',
        'email': 'test@test.com',

    }

@pytest.mark.asyncio
async def test_exception_update_user_forbidden(client, user, token):

    response = await client.put(
        f'/users/update/0',
        headers={'authorization': f'Bearer {token}'},
        json={
            'username': 'test2',
            'email': 'test@test.com',
        }
    )

    assert response.status_code == HTTPStatus.FORBIDDEN

@pytest.mark.asyncio
async def test_delete_user(client, user, token):
    response = await client.delete(
        f'/users/delete/{user.id}',
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "message": "user deleted"
    }

@pytest.mark.asyncio
async def test_exception_delete_user_forbidden(client, user, token):
    response =await client.delete(
        f'/users/delete/0',
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
