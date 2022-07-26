import pytest

from chat.models import ChatModel


class TestChatModel:
    @pytest.mark.django_db
    def test_chat(self):
        c = ChatModel.objects.create(sender='krisha', message='hii')
        assert c.sender == 'krisha'
        assert str(c) == c.message
