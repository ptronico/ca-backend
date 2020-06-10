import pytest


@pytest.mark.django_db
def test_user_created_signal(django_user_model):
    user = django_user_model.objects.create(username='user')
    assert hasattr(user, 'auth_token')

    user.save()  # just for 100% coverage
