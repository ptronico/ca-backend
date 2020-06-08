import pytest


@pytest.mark.django_db
def test_user_created_signal(django_user_model):
    user1 = django_user_model.objects.create(username='user1')
    assert hasattr(user1, 'auth_token')

    user1.save()  # just for 100% coverage
