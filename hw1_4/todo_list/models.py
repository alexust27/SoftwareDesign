from django.db import models


class TodoLists(models.Model):
    list_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.list_name


class TodoItem(models.Model):
    text = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)
    list_id = models.ForeignKey('TodoLists', on_delete=models.CASCADE)

    def __str__(self):
        return self.text
