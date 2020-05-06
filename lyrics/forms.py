from captcha.fields import ReCaptchaField
from .models import Post
from django import forms
from captcha.widgets import ReCaptchaV2Checkbox
from django.forms import ModelForm


class SubmitLyric(ModelForm):
    captcha = ReCaptchaField(required=True)

    class Meta:
        model = Post
        fields = [
            'username',
            'artist',
            'title',
            'album',
            'content',
            'captcha'
        ]

  #
  # widget=ReCaptchaV2Checkbox(
  #           attrs={
  #               'data-theme': 'dark',
  #               'data-size': 'compact',
  #           }
  #       )