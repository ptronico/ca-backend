import pytest

from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_user_created_signal(django_user_model):
    user1 = django_user_model.objects.create(username='user1')
    assert hasattr(user1, 'auth_token')

    user1.save()  # just for 100% coverage


@pytest.mark.django_db
def test_users_list(client, django_user_model):
    django_user_model.objects.create(username='user1')
    response = client.get(reverse('users-list'))
    assert 'api_token' not in response.data[0]
    assert response.status_code == 200


@pytest.mark.django_db
def test_users_create(client):
    response1 = client.post(reverse('users-list'), {'username': 'user1'})
    assert 'api_token' in response1.data
    assert response1.status_code == 201

    response2 = client.post(reverse('users-list'), {'username': 'user1'})
    assert 'api_token' not in response2.data
    assert response2.status_code == 400


@pytest.mark.django_db
def test_users_retrieve(client, admin_user, django_user_model):
    user1 = django_user_model.objects.create(username='user1')
    user2 = django_user_model.objects.create(username='user2')

    # Anon
    response1 = client.get(reverse('users-detail', args=['user1']))
    assert response1.status_code == 401

    # Other
    auth_token = 'Token %s' % user2.auth_token.key
    response2 = client.get(reverse('users-detail', args=['user1']), HTTP_AUTHORIZATION=auth_token)
    assert response2.status_code == 403

    # Owner
    auth_token = 'Token %s' % user1.auth_token.key
    response3 = client.get(reverse('users-detail', args=['user1']), HTTP_AUTHORIZATION=auth_token)
    assert response3.status_code == 200

    # Admin
    auth_token = 'Token %s' % admin_user.auth_token.key
    response4 = client.get(reverse('users-detail', args=['user1']), HTTP_AUTHORIZATION=auth_token)
    assert response4.status_code == 200
