from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import ChatModel

# Create your views here.


User = get_user_model()



@login_required
def ChatPage(request, id):
    user_obj = User.objects.get(id=id)
    users = User.objects.exclude(username=request.user.username)

    if request.user.id > user_obj.id:
        thread_name = f'chat_{request.user.id}-{user_obj.id}'
    else:
        thread_name = f'chat_{user_obj.id}-{request.user.id}'
    message_obj = ChatModel.objects.filter(thread_name=thread_name)
    return render(request, 'chat/main_chat.html', context={'users': users, 'user': user_obj, 'messages': message_obj})



