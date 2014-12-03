from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from mainsite.models import Message, Topic, Group, UserProfile, DirectMessage


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email',  'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'required': 'True',
                                               'size': 30,
                                               'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'required': 'True',
                                                   'size': 30,
                                                   'placeholder': 'Password'}),
            'email': forms.TextInput(attrs={'required': 'True',
                                            'size': 30,
                                            'placeholder': 'Email'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['username'].help_text = None
        self.fields['password'].label = ''
        self.fields['email'].label = ''
        self.fields['first_name'].label = ''
        self.fields['first_name'].widget.attrs['size'] = 30
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
        self.fields['last_name'].label = ''
        self.fields['last_name'].widget.attrs['size'] = 30
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        
    # Ensure e-mail is unique.
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['username'].widget.attrs['size'] = 30
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].label = ''
        self.fields['password'].widget.attrs['size'] = 30
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_description', 'school', 'notifications_enabled']

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
        exclude = ('creator', 'mod_set', 'user_set')
        fields = ('group_name', 'group_password')
        widgets = {
            'group_password': forms.PasswordInput(attrs={'required': 'True'}),
        }

class DirectMessageForm(forms.ModelForm):
    class Meta:
        model = DirectMessage
        exclude = ('pub_date', 'conversation', 'creator')
        widgets ={
            'message_content': forms.Textarea(attrs={'cols': 40, 'rows': 3,
                                                     'placeholder': "Write your message here...",
                                                     'required': 'True'})
        }


