from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class Order(models.Model):
	status = models.CharField(max_length = 100, choices=(('pending', 'Pending'), ('completed', 'Completed')), default='Pending')
	size = models.CharField(max_length = 100, choices=(('choose', ''), ('Small (12.70 $)', 'Small (12.70 $)'), ('Large 17.95 $', 'Large 17.95 $')), default='Size')
	type = models.CharField(max_length = 100, choices=(('choose ', ''), ('Regular (+ 0.00 $)', 'Regular (+ 0.00 $)'), ('Sicilian (+ 20.75 $)', 'Sicilian (+ 20.75 $)')), default='Type')
	toppings = models.CharField(max_length = 100, choices=(('choose', ''), ('Cheese (+ 0.00 $)', 'Cheese (+ 0.00 $)'), ('1 (+ 2.00 $)', '1 (+ 2.00 $)'), ('2 (+ 4.00 $)', '2 (+ 4.00 $)'), ('3 (+ 6.00 $)', '3 (+ 6.00 $)'), ('Special (+ 7.00 $)', 'Special (+ 7.00 $)')), default='Topping')
	smallSubs = models.CharField(max_length = 100, choices=(('choose', ''), ('Cheese (6.50 $)', 'Cheese (6.50 $)'), ('Italian (6.50 $)', 'Italian (6.50 $)'), ('Ham + Cheese (6.50 $)', 'Ham + Cheese (6.50 $)'), ('Meatball (6.50 $)', 'Meatball (6.50 $)'), ('Tuna (6.50 $)', 'Tuna (6.50 $)'), ('Turkey (6.50 $)', 'Turkey (6.50 $)'), ('Chicken Parmagiana (7.50 $)', 'Chicken Parmagiana (7.50 $)'), ('Eggplant Parmagian (6.50 $)', 'Eggplant Parmagian (6.50 $)'), ('Steak (6.50 $)', 'Steak (6.50 $)'), ('Steak + Cheese (6.95 $)', 'Steak + Cheese (6.95 $)'), ('Hamburger (4.60 $)', 'Hamburger (4.60 $)'), ('Cheeseburger (5.10 $)', 'Cheeseburger (5.10 $)'), ('Fried Chicken (6.95 $)', 'Fried Chicken (6.95 $)'), ('Veggie (6.95 $)', 'Veggie (6.95 $)')), default='sub')
	largeSubs = models.CharField(max_length = 100, choices=(('choose', ''), ('Cheese (7.95 $)', 'Cheese (7.95 $)'), ('Italian (7.95 $)', 'Italian (7.95 $)'), ('Ham + Cheese (7.95 $)', 'Ham + Cheese (7.95 $)'), ('Meatball (7.95 $)', 'Meatball (7.95 $)'), ('Tuna (7.95 $)', 'Tuna (7.95 $)'), ('Turkey (8.50 $)', 'Turkey (8.50 $)'), ('Chicken Parmagiana (8.50 $)', 'Chicken Parmagiana (8.50 $)'), ('Eggplant Parmagian (7.95 $)', 'Eggplant Parmagian (7.95 $)'), ('Steak (7.95 $)', 'Steak (7.95 $)'), ('Steak + Cheese (8.50 $)', 'Steak + Cheese (8.50 $)'), ('Sausage, Peppers & Onions (8.50 $)', 'Sausage, Peppers & Onions (8.50 $)'), ('Hamburger (6.95 $)', 'Hamburger (6.95 $)'), ('Cheeseburger (7.45 $)', 'Cheeseburger (7.45 $)'), ('Fried Chicken (8.50 $)', 'Fried Chicken (8.50 $)'), ('Veggie (8.50 $)', 'Veggie (8.50 $)')), default='sub')
	pastas = models.CharField(max_length = 100, choices=(('choose', ''), ('Baked Ziti w/ Mozzarella (6.50 $)', 'Baked Ziti w/ Mozzarella (6.50 $)'), ('Baked Ziti w/Meatballs (8.75 $)', 'Baked Ziti w/Meatballs (8.75 $)'), ('Baked Ziti w/Chicken (9.75 $)', 'Baked Ziti w/Chicken (9.75 $)')), default='Pasta')
	salads = models.CharField(max_length = 100, choices=(('choose', ''), ('Garden Salad (6.25 $)', 'Garden Salad (6.25 $)'), ('Greek Salad (8.25 $)', 'Greek Salad (8.25 $)'), ('Antipasto (8.25 $)', 'Antipasto (8.25 $)'), ('Salad w/Tuna (8.25 $)', 'Salad w/Tuna (8.25 $)')), default='Salad')
	smallPlatters = models.CharField(max_length = 100, choices=(('choose', ''), ('Garden Salad (35.00 $)', 'Garden Salad (35.00 $)'), ('Greek Salad (45.00 $)', 'Greek Salad (45.00 $)'), ('Antipasto (45.00 $)', 'Antipasto (45.00 $)'), ('Baked Ziti (35.00 $)', 'Baked Ziti (35.00 $)'), ('Meatball Parm (45.00 $)', 'Meatball Parm (45.00 $)'), ('Chicken Parm (45.00 $)', 'Chicken Parm (45.00 $)')), default='Platters') 
	largePlatters = models.CharField(max_length = 100, choices=(('choose', ''), ('Garden Salad (60.00 $)', 'Garden Salad (60.00 $)'), ('Greek Salad (70.00 $)', 'Greek Salad (70.00 $)'), ('Antipasto (70.00 $)', 'Antipasto (70.00 $)'), ('Baked Ziti (60.00 $)', 'Baked Ziti (60.00 $)'), ('Meatball Parm (70.00 $)', 'Meatball Parm (70.00 $)'), ('Chicken Parm (80.00 $)', 'Chicken Parm (80.00 $)')), default='Platters')
	

	def __str__(self):
		return self.status


class UserManager(BaseUserManager):

	def create_user(self, email, password):
		print(self.model)
		if email and password:
			user = self.model()
			user.set_password(password)
			user.save()
		return user

	def create_superuser(self, email, password):
		user = self.create_user(email, password)
		user.is_admin = True 
		user.save()
		return user

class User(AbstractBaseUser):

	email = models.EmailField(max_length = 300, unique=True)
	is_admin = models.BooleanField(default=True)

	objects = UserManager()

	USERNAME_FIELD = "email"

	def __str__(self):
		return "email {}" .format(self.email)


	@property
	def is_staff(self):
		return self.is_admin
	def has_module_perms(self, app_label):
		return True
	def has_perm(self, perm, obj=None):
		return True

	