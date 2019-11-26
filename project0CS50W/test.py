from taskmanager.models import Task
Task.objects.all()
my_task = Task.objects.get(name= "udelej ukolnicek")