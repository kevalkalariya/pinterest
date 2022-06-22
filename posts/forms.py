from django import forms
from .models import Pin,PinBoard


class PinForm(forms.ModelForm):
    class Meta:
        model = Pin
        fields = ['img', 'title', 'description', 'pin_category']
        # exclude = ('author', 'date_posted')

    # def save(self, request=None, commit=True):
    #     m = super(PinForm, self).save(commit=False)
    #     if request:
    #         m.author = request.user
    #     return m


class PinUpdateForm(forms.ModelForm):
    class Meta:
        model = Pin
        fields = ['title', 'description']

class PinBoardForm(forms.ModelForm):
    class Meta:
        model = PinBoard
        fields = ['board_name']

