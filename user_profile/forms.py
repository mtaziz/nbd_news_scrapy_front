from django import forms
from django.contrib.auth.models import User
from models import UserProfile


class UserForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        password = self.cleaned_data["password"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['user_favorite_crawl_media_sort'].widget.attrs['readonly'] = True
        self.fields['user_favorite_crawl_media'].widget.attrs['readonly'] = True
        self.fields['user_favorite_crawl_dir_sort'].widget.attrs['readonly'] = True

    class Meta:
        model = UserProfile
        fields = ('user_favorite_crawl_media_sort', 'user_favorite_crawl_media', 'user_favorite_crawl_dir_sort')
