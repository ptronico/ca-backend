import pytest

from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_listing_companies(client):
    resp = client.get(reverse('companies-list'))
    assert resp.status_code == 200


@pytest.mark.django_db
def test_user_permissions_on_creating_companies(client, admin_user, django_user_model):
    # Anon
    response = client.post(reverse('companies-list'), {'name': 'Apple'})
    assert response.status_code == 401

    # Logged
    user = django_user_model.objects.create(username='user')
    auth_token = 'Token %s' % user.auth_token.key
    user_response = client.post(reverse('companies-list'), {'name': 'Apple'}, HTTP_AUTHORIZATION=auth_token)
    assert user_response.status_code == 403

    # Admin request
    auth_token = 'Token %s' % admin_user.auth_token.key
    admin_response = client.post(reverse('companies-list'), {'name': 'Apple'}, HTTP_AUTHORIZATION=auth_token)
    assert admin_response.status_code == 201
