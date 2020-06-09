import pytest

from reviews.models import Review
from companies.models import Company


@pytest.mark.django_db
def test_review_str(django_user_model):
    """
    Test `Review.__str__` method.
    """
    user = django_user_model.objects.create(username='user1')
    company = Company.objects.create(name='company1')
    review = Review.objects.create(reviewer=user, company=company,
                                   title='Title', summary='Summary', rating=4, ipv4='127.0.0.1')
    assert str(review) == 'Title'
