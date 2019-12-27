from django.shortcuts import render, redirect, render_to_response
from django.views import generic
from .models import Rocket, Order
from .forms import Order


class Index(generic.ListView):
	template_name = "rockets/index.html"
	context_object_name = "rockets"

	def get_queryset(self):
		return Rocket.objects.all().order_by("name")

class DetailView(generic.DetailView):

	model = Rocket
	template_name = "rockets/detail.html"

class Order(generic.edit.CreateView):
	model = Rocket
	form_class = Order
	template_name = "rockets/order.html"

	def get(self, request, pk):
		form = self.form_class(None)
		return render(request, self.template_name, {"form":form})

	def post(self, request, pk):
		form = self.form_class(request.POST)
		if form.is_valid():
			form.save(commit=True)
		return render(request, "rockets/index.html", {"form"})





