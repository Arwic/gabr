from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from .models import Profile, Post, User
from nocaptcha_recaptcha.fields import NoReCaptchaField


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
        html = '<img src="{}" /> ' \
               '<label class="file">' \
               '<input type="file" name="{}" accept="image/gif,image/jpeg,image/jpg,image/png">' \
               '<span class="file-custom"></span>' \
               '</label>'\
                    .format(value.url, name)
        return mark_safe(html)


class HiddenWidget(widgets.Widget):
    def render(self, name, value, attrs=None):
        html = '<input type="hidden" name="{}"/>'.format(name)
        return mark_safe(html)


class SettingsProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'display_name',
            'avatar',
            'banner',
            'bio',
            'location',
            'website',
            'birthday',
        ]
        widgets = {
            'avatar': PictureSelectorWidget,
            'banner': PictureSelectorWidget,
            'birthday': widgets.DateInput(attrs={'type': 'date'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


CHOICES_GENDER = [(0, 'Male'), (1, 'Female')]


class SignupForm(forms.Form):
    username = forms.CharField()
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    display_name = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    gender = forms.ChoiceField(choices=CHOICES_GENDER)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'body',
            'target',
            'parent'
        ]
        widgets = {
            'body': PostWidget,
            'target': forms.HiddenInput,
            'parent': forms.HiddenInput
        }


class SettingsAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]


class SettingsNotificationsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [

        ]


class AxesCaptchaForm(forms.Form):
    captcha = NoReCaptchaField(gtag_attrs={'data-callback': 'onReCaptchaSuccess'})
