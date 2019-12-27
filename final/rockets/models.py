from django.db import models


class Manufacture(models.Model):
	manufacture = models.CharField(max_length = 300)
	origin = models.CharField(max_length = 200)

	def __str__(self):
		return "{0}".format(self.manufacture)

class Rocket(models.Model):
	image = models.ImageField()
	name = models.CharField(max_length=200)
	manufacture = models.ForeignKey(Manufacture, on_delete=models.SET_NULL, null=True)
	thrust = models.FloatField()
	payload = models.FloatField()
	description = models.TextField()

	def __str__(self):
		return "{0}".format(self.name)

class Order(models.Model):
	
	date = models.DateTimeField(auto_now=False)
	orbit = models.CharField(max_length = 200, choices=(
		('Low Orbit', 'Low Orbit'),
		('Geostationary Orbit', 'Geostationary Orbit'),
		('High Orbit', 'High Orbit'),
		('Moon', 'Moon'),
		('Mars', 'Mars')
		), default='orbit')
	site = models.CharField(max_length = 200, choices=(
		('Baikonur', 'Baikonur'),
		('Plesetsk','Plesetsk'),
		('Cape Canaveral','Cape Canaveral'),
		('Vanderberg', 'Vanderberg'),
		('Jiuquan', 'Jiuquan')
		), default='site')
	customerName = models.CharField(max_length = 500)
	note = models.TextField()

	def __str__(self):
		return "{0}".format(self.customerName)

