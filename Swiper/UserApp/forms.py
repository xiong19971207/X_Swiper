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

    def clean_max_distance(self):

        cleaned_data = super().clean()
        if cleaned_data['max_distance'] >= cleaned_data['min_distance']:
            return cleaned_data['max_distance']
        else:
            raise forms.ValidationError('最大距离不能小于最小距离')

    def clean_max_dating_age(self):

        cleaned_data = super().clean()
        if cleaned_data['max_dating_age'] >= cleaned_data['min_dating_age']:
            return cleaned_data['max_dating_age']
        else:
            raise forms.ValidationError('max_dating_age 不能小于 min_dating_age')
