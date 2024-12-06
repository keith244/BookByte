from django.db import models
import datetime
from datetime import timedelta
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Book(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    pdf_file = models.FileField(upload_to='pdfs/')
    upload_date = models.DateTimeField(auto_now_add=True)
    cover_pic = models.ImageField(upload_to='cover_pics/', blank=True)


    def __str__(self):
        return self.title
    
class ReadingProgress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    current_page = models.IntegerField(default=1)
    total_pages = models.IntegerField()
    last_read = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default = False)

    class Meta:
        unique_together = ['user', 'book']
    
    def __str__(self):
        return f'{self.user.username}--{self.book.title} ({self.current_page}/{self.total_pages})'
    
class Bookmark (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    page = models.IntegerField()
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.book.title} (Page {self.page})'