from django import forms

from UserApp.models import User, Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'gender', 'location', 'birthday']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
