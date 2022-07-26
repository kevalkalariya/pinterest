import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Pin, PinCategory, UserInterest, PinBoards, SavePin, Boards, Comments, Followers, Likes
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PinForm, PinBoardForm, CommentsForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views import View
from wsgiref.util import FileWrapper
import mimetypes
from django.db.models import Q
from django.core.paginator import Paginator

User = get_user_model()


class SearchPin(View):
    """this class for search pin"""

    def get(self, request):
        q = request.GET['q']
        pins = Pin.objects.filter(Q(title__icontains=q) | Q(author__username__icontains=q))
        if len(pins) == 0:
            pins = Pin.objects.all()
        return render(request, 'posts/home.html', {'pins': pins})


class InterestViewContent(ListView):
    """this class for Interest pins in home feed"""
    model = Pin
    template_name = 'posts/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(InterestViewContent, self).get_context_data(**kwargs)
        interest = UserInterest.objects.filter(user=self.request.user)
        # print(interest)
        if len(interest) > 0:
            pins = Pin.objects.filter(pin_category=interest[0].pin_cate)
            for i in interest[1:]:
                pins |= Pin.objects.filter(pin_category=i.pin_cate)
        else:
            pins = Pin.objects.all()

        boards = PinBoards.objects.filter(user_id=self.request.user.id)
        context['pins'] = pins
        context['boards'] = boards
        return context


class DateViewContent(ListView):
    """this class for view datewise pins"""
    model = Pin
    template_name = 'posts/home.html'
    context_object_name = "pins"
    ordering = ['-date_posted']
    paginator_class = Paginator
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DateViewContent, self).get_context_data(**kwargs)
        boards = PinBoards.objects.filter(user_id=self.request.user.id)
        context['boards'] = boards
        return context


class PinListView(ListView):
    """this class for pin view"""
    model = Pin
    template_name = 'posts/home.html'
    context_object_name = "pins"
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PinListView, self).get_context_data(**kwargs)
        boards = PinBoards.objects.filter(user_id=self.request.user.id)
        context['boards'] = boards
        return context


class UserPinListView(ListView):
    """this view class for another user profile view"""
    model = Pin
    template_name = 'posts/users_pins.html'
    context_object_name = 'pins'
    ordering = ['-date_posted']
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        pins = Pin.objects.filter(author_id=self.kwargs.get('pk')).order_by('-date_posted')
        context = {'pins': pins}
        return render(request, 'posts/users_pins.html', context=context)


class PinDetailView(DetailView):
    """this class for pin detail view"""
    model = Pin
    template_name = 'posts/pin_detail.html'
    form_class = CommentsForm

    def get(self, request, *args, **kwargs):
        pins = Pin.objects.filter(id=self.kwargs.get('pk')).order_by('-date_posted')
        comments = Comments.objects.filter(pin=self.kwargs.get('pk')).order_by('-date_posted')
        context = {'pins': pins, 'form': CommentsForm, 'comments': comments}
        return render(request, 'posts/pin_detail.html', context=context)

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.pin = Pin.objects.get(id=pk)
            form.user = request.user
            form.save()
            return redirect('pin-detail', pk=pk)


class PinCreateView(LoginRequiredMixin, View):
    """this class for create pin"""
    model = Pin
    form_class = PinForm
    template_name = "posts/pin_form.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            messages.info(request, f'Your Pin is successfully created!')
            return redirect('home')
        messages.error(request, f'Invalid data')
        return redirect('home')


class PinUpdateView(LoginRequiredMixin, UpdateView):
    """this class for update pin"""
    model = Pin
    fields = ['img', 'title', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect('home')


class GetInterest(View):
    """this class for get interest in home dropdown"""

    def post(self, request):
        interest = request.POST.getlist('interest')
        print(interest)
        for i in interest:
            cateid = PinCategory.objects.get(category_name=i)
            UserInterest.objects.create(pin_cate=cateid, user=request.user)
        return redirect('home')

    def get(self, request):
        context = {
            'pincate': PinCategory.objects.all()
        }

        return render(request, 'posts/interest_form.html', context)


class BoardCreateView(LoginRequiredMixin, CreateView):
    """this class for create board"""
    model = PinBoards
    form_class = PinBoardForm
    template_name = 'posts/pin_board.html'
    board_set = PinBoards.objects.all()

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            board_obj = PinBoards.objects.filter(user_id=request.user.id, board_name=form.cleaned_data['board_name'])
            if not board_obj:
                if form not in PinBoards.objects.all():
                    print(request.user)
                    form = form.save(commit=False)
                    form.user_id = request.user
                    form.save()
                    messages.info(request, f'Your board is created!')
                    return redirect('view-profile')
            else:
                messages.info(request, f'Board with same name already exists!')
                return redirect('board-create')


class SavePinProfile(View):
    """this class for save pin into profile"""

    def get(self, request, *args, **kwargs):
        user = request.user
        pin = self.kwargs.get('pk')
        SavePin.objects.create(user_id=user, pin_id=Pin.objects.get(id=pin))
        return redirect('view-profile')


class SaveToBoard(View):
    """this class for save pin into board"""

    def get(self, request, **kwargs):
        board_name = self.kwargs.get('board_name')
        pk = self.kwargs.get('pk')
        Boards.objects.create(board_id=PinBoards.objects.get(board_name=board_name),
                              pin_id=Pin.objects.get(pk=pk))
        return redirect('view-profile')


class ViewBoardPin(View):
    """this class for view board"""

    def get(self, request, board_name):
        board = Boards.objects.filter(board_id=PinBoards.objects.get(board_name=board_name))
        context = {'board_pin': board}
        return render(request, 'posts/board_pin_view.html', context=context)


class LikeView(LoginRequiredMixin, View):
    """this class for like pin"""
    def post(self, request):
        pin_id = request.POST['pid']
        print(pin_id)
        pin = Pin.objects.get(id=pin_id)
        is_liked = False
        if Likes.objects.filter(user=request.user, pin=pin).exists():
            Likes.objects.filter(user=request.user, pin=pin).delete()
        else:
            Likes.objects.create(user=request.user, pin=pin)
            is_liked = True
        total_likes = Likes.objects.filter(pin=pin_id).count()
        pin_instance = Pin.objects.get(id=pin_id)
        pin_instance.like_count = total_likes
        pin_instance.save()
        return JsonResponse({'is_liked': is_liked, 'total_likes': total_likes}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class PostUnfollowView(View):
    """this class for unfollow user"""

    def post(self, request, *args, **kwargs):
        request_data = request.read()
        form_data = json.loads(request_data.decode('utf-8'))
        author_id = form_data.get('author_id')
        print(author_id)
        receiver = User.objects.get(id=author_id)
        print(receiver)
        author = Followers.objects.filter(sender=request.user, receiver=receiver).first()
        author.is_follow = False
        author.save()
        return JsonResponse({'msg': 'Thank you for making me bored'})


@method_decorator(csrf_exempt, name='dispatch')
class PostFollowView(View):
    """this class for follow user"""

    def post(self, request, *args, **kwargs):
        request_data = request.read()
        form_data = json.loads(request_data.decode('utf-8'))
        author_id = form_data.get('author_id')
        print(author_id)
        receiver = User.objects.get(id=author_id)
        print(receiver)
        follower_exist = Followers.objects.filter(sender=request.user, receiver=receiver).first()
        if follower_exist:
            follower_exist.is_follow = True
            follower_exist.save()
        else:
            author = Followers.objects.create(sender=request.user, receiver=receiver, is_follow=True)
            author.save()
        return JsonResponse({'msg': 'Thank you for making me bored'})


def download_image(request, id):
    """this class for download pin"""
    img = Pin.objects.get(id=id)
    wrapper = FileWrapper(img.img.file)  # img.file returns full path to the image
    content_type = mimetypes.guess_type(img.img.name)[0]  # Use mimetypes to get file type
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Disposition'] = "attachment; filename=%s" % img.title
    return response


class DeletePin(DeleteView, LoginRequiredMixin):
    """this class for delete pin"""

    def get(self, request, id):
        pin = Pin.objects.get(id=id)
        pin.delete()
        return redirect('view-profile')


class ViewInterest(View):
    """this class for view interest into interest update page"""

    def get(self, request):
        interest = PinCategory.objects.all()
        myinterest = UserInterest.objects.filter(user_id=request.user)
        return render(request, 'posts/Interest_update.html', {'interest': interest, 'myinterest': myinterest})


class AddInterest(View):
    """this class for add interest into user interest feed"""

    def get(self, request, id):
        try:
            UserInterest.objects.get(pin_cate_id=id, user=request.user)
            messages.error(request, 'already exists')
            return redirect('view-interest')
        except:
            UserInterest.objects.create(pin_cate_id=id, user=request.user)
        return redirect('view-interest')


class DeleteInterest(View):
    """this class for delete interest into user interest feed"""

    def get(self, request, id):
        interest = UserInterest.objects.filter(pin_cate_id=id, user=request.user).delete()
        return redirect('view-interest')
