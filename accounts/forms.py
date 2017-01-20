from django import forms
from django.contrib.auth import (
    get_user_model,
)


User = get_user_model()
class LoginForm(forms.Form):
    username = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),label="")


    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user_qs = User.objects.filter(username=username) #queries to get username
        if user_qs.count() == 1:
            user = user_qs.first() #if found username assign to user
        else:
            user = None
            raise forms.ValidationError("The user does not exist") #raise error saying user doesnt exist

        if user is not None:
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password")
            if not user.is_active:
                raise forms.ValidationError("The User is no longer employeed")
            return super(LoginForm, self).clean(*args, **kwargs)




