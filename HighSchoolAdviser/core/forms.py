from django import forms

# deprecated
class RegistrationForm(forms.Form):
    email = forms.EmailField(label='E-mail', max_length=50)
    password = forms.CharField(label='Пароль', max_length=50, widget=forms.PasswordInput)