import pytest

from posts.models import PinCategory, Pin, PinBoards
from users.models import User, Profile


@pytest.fixture
def create_user(db, client):
    """Fixture for creating user"""

    def make_user():
        new_user = User.objects.create_user(email='krisha@gmail.com', password='Testing321@')
        return new_user

    return make_user


@pytest.fixture
def create_profile(create_user):
    """Fixture for creating profile"""

    def make_profile():
        profile = Profile.objects.get_or_create(user=create_user(), firstname='Hetvee', lastname='shah', about='my frd',
                                                website='h.com')[0]
        return profile

    return make_profile


@pytest.fixture
def create_category():
    def make_category():
        category = PinCategory.objects.create(category_name='marvel')

        return category

    return make_category


@pytest.fixture
def create_pin(create_profile, create_user, create_category):
    """Fixture for creating pin"""

    def make_pin(author=None):
        if author is None:
            author = create_user()
        pin = Pin.objects.create(title='star', description='shining', author=author,
                                 pin_category=create_category())
        return pin

    return make_pin


@pytest.fixture
def create_board(create_category, create_pin, create_user):
    def make_pinboard(user_id=None):
        if user_id is None:
            user_id = create_user()
        board = PinBoards.objects.create(board_name='thor', user_id=user_id)
        return board

    return make_pinboard


