import pytest
from users.models import User, Profile


class TestProfile:
    @pytest.mark.django_db
    def test_profile(self):
        u = User.objects.create_user(email='krisha@gmail.com', password='Testing321@')
        p = Profile.objects.create(user=u, firstname='krisha')
        assert p.user.email == 'krisha@gmail.com'
        assert p.firstname == 'krisha'
        assert str(p) == p.user.email

    @pytest.mark.django_db
    def test_superuser(self):
        s = User.objects.create_superuser(email='jack@gmail.com',password='admin')
        s.is_staff = True
