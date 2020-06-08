import pytest

from companies.models import Company


@pytest.mark.django_db
def test_company_str():
    """
    Test `Company.__str__` method.
    """
    apple = Company.objects.create(name='Apple')
    assert str(apple) == 'Apple'
