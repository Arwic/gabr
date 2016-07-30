from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from .models import UserProfile, Post, Message


class PostWidget(widgets.Textarea):
    def render(self, name, value, attrs=None):
        html = '<textarea class="form-control" style="width: 540px;" rows="3" cols="75" name="{}" maxlength="140"></textarea>' \
                    .format(attrs['id'][3:])
        return mark_safe(html)


class PictureWidget(widgets.Widget):
    def render(self, name, value, attrs=None):
        html = '<img src="{}" width="64" />'\
            .format(value.url)
        return mark_safe(html)


class PictureSelectorWidget(widgets.ClearableFileInput):
    def render(self, name, value, attrs=None):
        html = '<img src="{}" width="64" /> ' \
               '<label class="file">' \
               '<input type="file" id="file" name="{}" accept="image/gif,image/jpeg,image/jpg,image/png">' \
               '<span class="file-custom"></span>' \
               '</label>'\
                    .format(value.url, attrs['id'][3:])
        return mark_safe(html)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'display_name',
            'avatar',
            'banner',
            'bio',
            'location',
            'website',
            'birthday',
            'time_zone',
        ]
        widgets = {
            'avatar': PictureSelectorWidget,
            'banner': PictureSelectorWidget,
        }


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


CHOICES_GENDER = [(0, 'Male'), (1, 'Female')]


class SignupForm(forms.Form):
    username = forms.CharField()
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    gender = forms.ChoiceField(choices=CHOICES_GENDER, widget=forms.RadioSelect())


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'body',
        ]
        widgets = {
            'body': PostWidget,
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            'target',
            'body',
        ]
