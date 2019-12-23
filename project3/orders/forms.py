from django import forms
from .models import Order, User

class Form(forms.ModelForm):

	class Meta:
		model = Order
		fields = ('size', 'type', 'toppings', 'smallSubs', 'largeSubs', 'pastas', 'salads', 'smallPlatters', 'largePlatters')


class UserForm(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput)
	class Meta:
		model = User
		fields = ['email', 'password']

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        fields = ["email", "password"]