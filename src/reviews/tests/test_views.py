import pytest

from rest_framework.reverse import reverse

from companies.models import Company

from ..models import Review


@pytest.mark.django_db
def test_reviews_list(client, django_user_model):
    user1 = django_user_model.objects.create(username='user1')
    user2 = django_user_model.objects.create(username='user2')

    # Other
    auth_token = 'Token %s' % user2.auth_token.key
    response = client.get(reverse('users-reviews-list', args=['user1']), HTTP_AUTHORIZATION=auth_token)
    assert response.status_code == 403

    # Owner
    auth_token = 'Token %s' % user1.auth_token.key
    response = client.get(reverse('users-reviews-list', args=['user1']), HTTP_AUTHORIZATION=auth_token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_reviews_create(client, django_user_model):
    company = Company.objects.create(name='Apple')
    user1 = django_user_model.objects.create(username='user1')
    user2 = django_user_model.objects.create(username='user2')

    payload = {
        'company_id': company.pk,
        'title': 'Good products!',
        'summary': '...',
        'rating': 4,
        'ipv4': '127.0.0.1',
    }

    invalid_payload = {
        'company_id': 2000,
        'title': '',
        'summary': '',
        'rating': 6,
    }

    # Anon
    response = client.post(reverse('users-reviews-list', args=['user1']), payload)
    assert response.status_code == 401

    # Other
    auth_token = 'Token %s' % user2.auth_token.key
    response = client.post(reverse('users-reviews-list', args=['user1']), payload, HTTP_AUTHORIZATION=auth_token)
    assert response.status_code == 403

    # Owner (invalid payload)
    auth_token = 'Token %s' % user1.auth_token.key
    response = client.post(reverse('users-reviews-list', args=['user1']),
                           invalid_payload, HTTP_AUTHORIZATION=auth_token)
    assert response.status_code == 400

    # Owner
    auth_token = 'Token %s' % user1.auth_token.key
    response = client.post(reverse('users-reviews-list', args=['user1']), payload, HTTP_AUTHORIZATION=auth_token)
    assert response.status_code == 201


@pytest.mark.django_db
def test_reviews_retrieve(client, admin_user, django_user_model):
    company = Company.objects.create(name='Apple')
    user1 = django_user_model.objects.create(username='user1')
    user2 = django_user_model.objects.create(username='user2')
    review = Review.objects.create(reviewer=user1, company=company,
                                   title='Good products', summary='...', rating=4, ipv4='127.0.0.1')

    # Anon
    response1 = client.get(reverse('users-reviews-detail', args=['user1', review.pk]))
    assert response1.status_code == 401

    # Other
    auth_token = 'Token %s' % user2.auth_token.key
    response2 = client.get(reverse('users-reviews-detail', args=['user1', review.pk]), HTTP_AUTHORIZATION=auth_token)
    assert response2.status_code == 403

    # Owner
    auth_token = 'Token %s' % user1.auth_token.key
    response3 = client.get(reverse('users-reviews-detail', args=['user1', review.pk]), HTTP_AUTHORIZATION=auth_token)
    assert response3.status_code == 200

    # Admin
    auth_token = 'Token %s' % admin_user.auth_token.key
    response4 = client.get(reverse('users-reviews-detail', args=['user1', review.pk]), HTTP_AUTHORIZATION=auth_token)
    assert response4.status_code == 200
