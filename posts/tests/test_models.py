import pytest
from users.models import User
from posts.models import PinCategory, Pin, UserInterest, PinBoards, Boards, SavePin, Comments


class TestPinCategory:
    @pytest.mark.django_db
    def test_pincategory(self):
        c = PinCategory.objects.create(category_name='art')
        assert c.category_name == 'art'
        assert str(c) == c.category_name


class TestPin:
    @pytest.mark.django_db
    def test_pin(self):
        u = User.objects.create(email='krisha@gmail.com', password='Testing321@')
        c = PinCategory.objects.create(category_name='art')
        p = Pin.objects.create(title='Hetveee', description='is my frd', author=u, pin_category=c, like_count=2)
        assert u.email == 'krisha@gmail.com'
        assert c.category_name == 'art'
        assert p.title == 'Hetveee'
        assert p.description == 'is my frd'
        assert str(p) == p.title


class TestUserInterest:
    @pytest.mark.django_db
    def test_userinterest(self):
        u = User.objects.create(email='krisha@gmail.com', password='Testing321@')
        c = PinCategory.objects.create(category_name='art')
        i = UserInterest.objects.create(user=u, pin_cate=c)
        assert i.user.email == 'krisha@gmail.com'
        assert i.pin_cate.category_name == 'art'


class TestPinBoards:
    @pytest.mark.django_db
    def test_pinboards(self):
        u = User.objects.create(email='krisha@gmail.com', password='Testing321@')
        b = PinBoards.objects.create(board_name='marvel', user_id=u)
        assert b.board_name == 'marvel'
        assert b.user_id.email == 'krisha@gmail.com'
        assert str(b) == b.board_name


class TestBoard:
    @pytest.mark.django_db
    def test_boards(self):
        u = User.objects.create(email='krisha@gmail.com', password='Testing321@')
        b = PinBoards.objects.create(board_name='marvel', user_id=u)
        c = PinCategory.objects.create(category_name='art')
        p = Pin.objects.create(title='Hetveee', description='is my frd', author=u, pin_category=c, like_count=2)
        s = Boards.objects.create(board_id=b, pin_id=p)
        assert s.board_id.board_name == 'marvel'
        assert s.pin_id.title == 'Hetveee'


class TestSavePin:
    @pytest.mark.django_db
    def test_savepin(self):
        u = User.objects.create(email='krisha@gmail.com', password='Testing321@')
        c = PinCategory.objects.create(category_name='art')
        p = Pin.objects.create(title='Hetveee', description='is my frd', author=u, pin_category=c, like_count=2)
        s = SavePin.objects.create(user_id=u, pin_id=p)
        assert s.user_id.email == 'krisha@gmail.com'
        assert s.pin_id.title == 'Hetveee'


class TestComments:
    @pytest.mark.django_db
    def test_comments(self):
        u = User.objects.create(email='krisha@gmail.com', password='Testing321@')
        c = PinCategory.objects.create(category_name='art')
        p = Pin.objects.create(title='Hetveee', description='is my frd', author=u, pin_category=c, like_count=2)
        s = Comments.objects.create(user=u, pin=p, comment='hii')
        assert s.user.email == 'krisha@gmail.com'
        assert s.pin.title == 'Hetveee'
        assert s.comment == 'hii'
