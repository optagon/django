from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render, reverse, redirect
from .forms import Form, UserForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from .models import Order, User


# Create your views here.
def index(request):

	if request.method == "POST":
		form = Form(request.POST)
		if form.is_valid():
			form.save()

	form = Form()
	return render(request, "orders/index.html", {'form':form})

def checkout(request):

	obj = Order.objects.latest("id")
	context = {
		'size': obj.size,
		'type': obj.type,
		'toppings': obj.toppings,
		'smallSubs': obj.smallSubs,
		'largeSubs': obj.largeSubs,
		'pastas': obj.pastas,
		'salads': obj.salads,
		'smallPlatters': obj.smallPlatters,
		'largePlatters': obj.largePlatters,
	}
	
	return render(request, "orders/checkout.html", context)

def submited(request):
	return render(request, "orders/submited.html")

class UserViewRegister(generic.edit.CreateView):
	form_class = UserForm
	model = User
	template_name = "orders/user_form.html"

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {"form": form})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			user = form.save(commit = False)
			password = form.cleaned_data["password"]
			user.set_password(password)
			user.save()
			login(request, user)
			return redirect("index")

		return render(request, self.template_name, {"form":form})

class UserViewLogin(generic.edit.CreateView):
	form_class = LoginForm
	template_name = "orders/user_form.html"

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {"form": form})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			email = form.cleaned_data["email"]
			password = form.cleaned_data["password"]
			user = authenticate(email = email, password = password)
		if user:
				login(request, user)
				return redirect("index")
		return render(request, self.template_name, {"form": form})

def logout_user(request):
		logout(request)
		return redirect(reverse("login"))


