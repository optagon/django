from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.Index.as_view(), name="index"),
	path('<int:pk>/detail', views.DetailView.as_view(), name="detail"),
	path('<int:pk>/order', views.Order.as_view(), name="order"),

]