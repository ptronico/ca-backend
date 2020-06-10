import pytest

from django import urls

from rest_framework.reverse import reverse


@pytest.mark.parametrize('view_name', ['go-to-api'])
def test_redirect_from_root_to_api(view_name, client):
    url = urls.reverse(view_name)
    resp = client.get(url)
    assert resp.status_code == 302


@pytest.mark.django_db
def test_listing_users(client, django_user_model):
    django_user_model.objects.create(username='user')
    response = client.get(reverse('users-list'))
    assert 'api_token' not in response.data[0]
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize('username, expected', [('user1', 201), ('user2', 400), ('user*', 400), ('!@#$', 400)])
def test_creating_users(username, expected, client, django_user_model):
    django_user_model.objects.create(username='user2')
    response = client.post(reverse('users-list'), {'username': username})
    assert response.status_code == expected


@pytest.mark.django_db
def test_user_permissions_on_retrieving_users(client, admin_user, django_user_model):
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
