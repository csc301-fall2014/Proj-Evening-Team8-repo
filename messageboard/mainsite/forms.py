from django import forms
from django.contrib.auth.models import User
from mainsite.models import Message, Topic, Group, UserProfile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email',  'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'required': 'True'}),
            'password': forms.PasswordInput(attrs={'required': 'True'}),
            'email': forms.TextInput(attrs={'required': 'True'}),
        }

    # Ensure e-mail is unique.
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'activation_key', 'key_expires', 'timejoined')

    # Ensure e-mail is unique.
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        exclude = ('pub_date', 'creator', 'subscriptions')
        fields = ('topic_name', 'group_set')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields['group_set'].widget = forms.CheckboxSelectMultiple()
        self.fields['group_set'].help_text = "Select which group's users are allowed to see this topic, or none to make this topic public."
        self.fields['group_set'].queryset = user.joined_groups


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ('creator', 'user_set')
        fields = ('group_name', 'group_password')
        widgets = {
            'group_password': forms.PasswordInput(attrs={'required': 'True'}),
        }


