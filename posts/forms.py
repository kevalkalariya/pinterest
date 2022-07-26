from django import forms
from .models import Pin, PinBoards, Comments


class PinForm(forms.ModelForm):
    class Meta:
        model = Pin
        fields = ['img', 'title', 'description', 'pin_category']


class PinUpdateForm(forms.ModelForm):
    class Meta:
        model = Pin
        fields = ['title', 'description']


class PinBoardForm(forms.ModelForm):
    class Meta:
        model = PinBoards
        fields = ['board_name']


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
