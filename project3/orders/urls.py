from django.urls import path, include
from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("checkout", views.checkout, name="checkout"),
	path("submited", views.submited, name="submited"),
	path("register/", views.UserViewRegister.as_view(), name = "regiser"),
	path("login/", views.UserViewLogin.as_view(), name = "login"),
	path("logout/", views.logout_user, name = "logout"),
]




