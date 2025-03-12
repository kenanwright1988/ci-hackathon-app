from django.db import models

# Create your models here.
class Challenge(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=20)
    points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    published_date = models.DateTimeField()
    suggested_solution = models.TextField()
    def __str__(self):
        return self.title