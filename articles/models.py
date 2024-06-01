from django.db import models
from profiles.models import User


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', default='articles/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return f'({self.id}) {self.title} - {self.author}'
