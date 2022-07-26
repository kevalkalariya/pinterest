import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from posts.models import UserInterest


class TestPinListView:
    @pytest.mark.django_db
    def test_pinlist(self, client, create_pin):
        p = create_pin()
        assert p.title == 'star'
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'posts/home.html')


class TestUserPinListView:
    @pytest.mark.django_db
    def test_userpinlistview(self, client, create_pin, create_profile):
        pin = create_pin()
        response = client.get(reverse('user-pins', kwargs={'pk': pin.pk}))
        assert response.status_code == 200
        assertTemplateUsed(response, 'posts/users_pins.html')


class TestPinDetailView:
    @pytest.mark.django_db
    def test_pindetailview(self, client, create_pin, create_profile):
        p = create_profile()
        pin = create_pin(author=p.user)
        client.login(email=p.user.email, password='Testing321@')
        response = client.get(reverse('pin-detail', kwargs={'pk': pin.pk}))
        assert response.status_code == 200
        assertTemplateUsed(response, 'posts/pin_detail.html')
        response = client.post(reverse('pin-detail', kwargs={'pk': pin.pk}),
                               data={'user': p.user.id, 'pin': pin.id, 'comment': 'hii'})
        assert response.status_code == 302


class TestSearchPin:
    @pytest.mark.django_db
    def test_searchpin(self, client):
        r = client.get(reverse('search'), {'q': 'star'})
        assert r.status_code == 200
        assertTemplateUsed(r, 'posts/home.html')
        response = client.get(reverse('search'), {'q': 'star'})
        assert response.status_code == 200
        assertTemplateUsed(response, 'posts/home.html')


class TestPinCreate:
    @pytest.mark.django_db
    def test_pincreate(self, client, create_pin, create_category, create_profile):
        p = create_profile()
        client.login(email=p.user.email, password='Testing321@')
        response = client.post(reverse('pin-create'),
                               data={'title': 'star', 'description': 'shining',
                                     'pin_category': create_category().id})
        assert response.status_code == 302
        assert (response, 'posts/pin_form.html')
        response = client.post(reverse('pin-create'),
                               data={'description': 'shining',
                                     'pin_category': create_category().id})
        assert response.status_code == 302
        assert (response, 'posts/home.html')


class TestPinUpdate:
    @pytest.mark.django_db
    def test_pinupdate(self, client, create_profile, create_pin):
        p = create_profile()
        pin = create_pin(author=p.user)
        client.login(email=p.user.email, password='Testing321@')
        response = client.post(reverse('pin-update', kwargs={'pk': pin.pk}),
                               data={'title': 'thor', 'description': 'marvelhero'})
        assert response.status_code == 302
        assert (response, 'posts/home.html')


class TestBoardCreate:
    @pytest.mark.django_db
    def test_boardcreate(self, client, create_profile):
        p = create_profile()
        client.login(email=p.user.email, password='Testing321@')
        response = client.post(reverse('board-create'),
                               data={'board_name': 'marvel', 'user_id': p.id})
        assert response.status_code == 302
        assert (response, 'users/view_profile.html')
        response = client.post(reverse('board-create'),
                               data={'board_name': 'marvel'})
        assert response.status_code == 302
        assert (response, 'posts/pin_board.html')


class TestSavePinProfile:
    @pytest.mark.django_db
    def test_savepinprofile(self, create_profile, client, create_pin):
        p = create_profile()
        pin = create_pin(author=p.user)
        client.login(email=p.user.email, password='Testing321@')
        response = client.get(reverse('save-pin', kwargs={'pk': pin.pk}),
                              data={'user_id': p.user.id, 'pin_id': pin.id})
        assert response.status_code == 302
        assert (response, 'users/view_profile.html')


class TestSaveToBoard:
    @pytest.mark.django_db
    def test_Savetoboard(self, create_profile, create_board, create_pin, client):
        p = create_profile()
        pin = create_pin(author=p.user)
        b = create_board(user_id=p.user)
        client.login(email=p.user.email, password='Testing321@')
        response = client.get(reverse('dropdown-board', kwargs={'pk': pin.pk, 'board_name': b.board_name}),
                              data={'board_id': b.id, 'pin_id': pin.id})
        assert response.status_code == 302
        assert (response, 'users/view_profile.html')


class TestViewBoardPin:
    @pytest.mark.django_db
    def test_viewboardpin(self, client, create_board, create_profile):
        p = create_profile()
        b = create_board(user_id=p.user)
        response = client.get(reverse('view-board-pin', kwargs={'board_name': b.board_name}))
        assert response.status_code == 200
        assertTemplateUsed(response, 'posts/board_pin_view.html')


class TestDeletePin:
    @pytest.mark.django_db
    def test_deletepin(self, client, create_pin, create_profile):
        p = create_profile()
        pin = create_pin(author=p.user)
        response = client.get(reverse('delete-pin', kwargs={'id': pin.pk}))
        assert response.status_code == 302


class TestLikeView:
    @pytest.mark.django_db
    def test_likeview(self, client, create_pin, create_profile):
        p = create_profile()
        client.login(email=p.user.email, password='Testing321@')
        pin = create_pin(author=p.user)
        response = client.post(reverse('pin-like'), data={'pid': pin.pk})
        assert response.status_code == 200
        response = client.post(reverse('pin-like'), data={'pid': pin.pk})
        assert response.status_code == 200


class TestGetInterest:
    @pytest.mark.django_db
    def test_getinterest(self, client, create_category, create_profile):
        p = create_profile()
        c = create_category()
        client.login(email=p.user.email, password='Testing321@')
        response = client.post(reverse('interest'), data={'interest': c.category_name})
        assert response.status_code == 302
        response = client.get(reverse('interest'),  data={'interest': c.category_name})
        assert response.status_code == 200


class TestViewInterest:
    @pytest.mark.django_db
    def test_viewinterest(self, client, create_profile):
        p = create_profile()
        client.login(email=p.user.email, password='Testing321@')
        response = client.get(reverse('view-interest'))
        assert response.status_code == 200


class TestAddInterest:
    @pytest.mark.django_db
    def test_addinterest(self, client, create_profile, create_category):
        p = create_profile()
        c = create_category()
        client.login(email=p.user.email, password='Testing321@')
        response = client.get(reverse('add-interest', kwargs={'id': c.id}))
        assert response.status_code == 302
        response = client.get(reverse('add-interest', kwargs={'id': c.id}))
        assert response.status_code == 302


class TestDeleteInterest:
    @pytest.mark.django_db
    def test_deleteinterest(self, client, create_profile, create_category):
        p = create_profile()
        c = create_category()
        client.login(email=p.user.email, password='Testing321@')
        response = client.get(reverse('delete-interest', kwargs={'id': c.id}))
        assert response.status_code == 302





class TestDateViewContent:
    @pytest.mark.django_db
    def test_dateviewcontent(self, client):
        response = client.get(reverse('datawise_content'))
        assert response.status_code == 200


class TestDownloadImange:
    @pytest.mark.django_db
    def test_downloadimage(self, client, create_profile, create_pin):
        p = create_profile()
        client.login(email=p.user.email, password='Testing321@')
        pin = create_pin(author=p.user)
        response = client.get(reverse('download-pin', kwargs={'id': pin.id}))
        assert response.status_code == 200

class TestInterestViewContent:
    @pytest.mark.django_db
    def test_interestview(self, client, create_profile, create_category,create_pin):
        p = create_profile()
        pin = create_pin(author=p.user)
        pin1 = create_pin(author=p.user)
        c = create_category()
        c1 = create_category()
        # client.login(email=p.user.email, password='Testing321@')

        client.login(email=p.user.email, password='Testing321@')
        esponse = client.get(reverse('interestwise_content'))
        assert esponse.status_code == 200
        # UserInterest.objects.create(user=p.user, pin_cate=c)
        # print(UserInterest.objects.all())

        UserInterest.objects.create(user=p.user,pin_cate=c)
        print(UserInterest.objects.all())


        response = client.get(reverse('interestwise_content'))

        assert response.status_code == 200