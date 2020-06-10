import pytest

from rest_framework.reverse import reverse

from companies.models import Company

from ..models import Review


@pytest.mark.django_db
def test_listing_reviews(client, django_user_model):
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
def test_user_permissions_on_creating_reviews(client, django_user_model):
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

    # Anon
    response = client.post(reverse('users-reviews-list', args=['user1']), payload)
    assert response.status_code == 401

    # Other
    auth_token = 'Token %s' % user2.auth_token.key
    response = client.post(reverse('users-reviews-list', args=['user1']), payload, HTTP_AUTHORIZATION=auth_token)
    assert response.status_code == 403

    # Owner
    auth_token = 'Token %s' % user1.auth_token.key
    response = client.post(reverse('users-reviews-list', args=['user1']), payload, HTTP_AUTHORIZATION=auth_token)
    assert response.status_code == 201


@pytest.mark.django_db
def test_user_permissions_on_retrieving_reviews(client, admin_user, django_user_model):
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


@pytest.mark.django_db
@pytest.mark.parametrize('payload, expected', [
    ({  # Good payload
        'company_id': 1,
        'rating': 4,
        'title': 'Morbi eget urna at diam',
        'summary': 'Mauris in viverra sapien. Morbi a ...',
    }, 201),
    ({  # Wrong company
        'company_id': 99,
        'rating': 4,
        'title': 'Morbi eget urna at diam',
        'summary': 'Mauris in viverra sapien. Morbi a ...',
    }, 400),
    ({  # Wrong rating
        'company_id': 1,
        'rating': 0,
        'title': 'Morbi eget urna at diam',
        'summary': 'Mauris in viverra sapien. Morbi a ...',
    }, 400),
    ({  # Wrong rating
        'company_id': 1,
        'rating': 6,
        'title': 'Morbi eget urna at diam',
        'summary': 'Mauris in viverra sapien. Morbi a ...',
    }, 400),
    ({  # Wrong title
        'company_id': 1,
        'rating': 3,
        'title': '',
        'summary': 'Mauris in viverra sapien. Morbi a ...',
    }, 400),
    ({  # Wrong title
        'company_id': 1,
        'rating': 3,
        'title': 'a' * (Review.title.field.max_length + 1),
        'summary': 'Mauris in viverra sapien. Morbi a ...',
    }, 400),
    ({  # Wrong summary
        'company_id': 1,
        'rating': 3,
        'title': 'Aenean quis lorem neque.',
        'summary': '',
    }, 400),
    ({  # Wrong summary
        'company_id': 1,
        'rating': 3,
        'title': 'Aenean quis lorem neque.',
        'summary': 'a' * (Review.summary.field.max_length + 1),
    }, 400),
])
def test_data_validation_on_creating_reviews(payload, expected, client, django_user_model):
    Company.objects.create(name='Apple')
    user = django_user_model.objects.create(username='user')
    auth_token = 'Token %s' % user.auth_token.key
    response = client.post(reverse('users-reviews-list', args=[user.username]),
                           payload, HTTP_AUTHORIZATION=auth_token)
    assert response.status_code == expected
