from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Pin, PinCategory, UserInterest,PinBoard
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PinForm,PinBoardForm
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.
def home(request):
    context = {
        'pins': Pin.objects.all()
    }
    return render(request, 'posts/home.html', context)


class PinListView(ListView):
    model = Pin
    template_name = 'posts/home.html'
    context_object_name = 'pins'
    ordering = ['-date_posted']

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Pin.objects.all()
        else:
            interest = UserInterest.objects.filter(user=self.request.user)
            print(interest)
            if len(interest) > 0:
                query_result = Pin.objects.filter(pin_category=interest[0].pin_cate)
                for i in interest[1:]:
                    query_result |= Pin.objects.filter(pin_category=i.pin_cate)
                    # interest_list += [i.pin_cate.category_name]
                print(query_result)

                return query_result
            else:
                return Pin.objects.all()


class UserPinListView(ListView):
    model = Pin
    template_name = 'posts/users_pins.html'
    context_object_name = 'pins'
    ordering = ['-date_posted']

    # def get_queryset(self):
    #     user = User.objects.filter(username=self.kwargs.get('username')).first()
    #     print(self.kwargs.get('username'))
    #     # user = get_object_or_404(User, username=self.kwargs.get('username'))
    #     print(user)
    #     return Pin.objects.filter(author=user).order_by('-date_posted')

    def get(self, request, *args, **kwargs):
        pins = Pin.objects.filter(author_id=self.kwargs.get('pk')).order_by('-date_posted')
        context = {'pins': pins}
        return render(request, 'posts/users_pins.html', context=context)


class PinDetailView(DetailView):
    model = Pin
    template_name = 'posts/pin_detail.html'

    def get(self, request, *args, **kwargs):
        pins = Pin.objects.filter(id=self.kwargs.get('pk')).order_by('-date_posted')
        context = {'pins': pins}
        return render(request, 'posts/pin_detail.html', context=context)


class PinCreateView(LoginRequiredMixin, CreateView):
    model = Pin
    form_class = PinForm
    template_name = "posts/pin_form.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            print(request.user)
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            messages.info(request, f'Your Pin is sucessfully created!')
            return redirect('home')


class PinUpdateView(LoginRequiredMixin, UpdateView):
    model = Pin
    fields = ['img', 'title', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect('home')


def interest_view(request):
    if request.method == 'POST':
        interest = request.POST.getlist('interest')
        for i in interest:
            cateid = PinCategory.objects.get(category_name=i)
            UserInterest.objects.create(pin_cate=cateid, user=request.user)
        return redirect('home')
    context = {
        'pincate': PinCategory.objects.all()
    }

    return render(request, 'posts/interest_form.html', context)

class BoardCreateView(LoginRequiredMixin,CreateView):
    model = PinBoard
    form_class = PinBoardForm
    template_name = 'posts/pin_board.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            print(request.user)
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            messages.info(request, f'Your board is created!')
            return redirect('view-profile')


