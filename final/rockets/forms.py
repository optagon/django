from django import forms
from .models import Order

class Order(forms.ModelForm):

	class Meta:
		model = Order
		fields = ["date", "orbit", "site", "customerName", "note"]