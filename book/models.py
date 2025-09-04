# BookByte - Copyright (C) 2025 Keith Kk
# Licensed under GNU GPLv3. See LICENSE for details.

from django.db import models
import datetime
from datetime import timedelta
from django.contrib.auth import get_user_model
import uuid

# Create your models here.

User = get_user_model()

class Book(models.Model):
    # uploaded_by = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)# default=uuid.UUID('9e3e8ec0614c47aba28f6200893d8137')) # type: ignore
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    pdf_file = models.FileField(upload_to='pdfs/')
    upload_date = models.DateTimeField(auto_now_add=True)
    cover_pic = models.ImageField(upload_to='cover_pics/', blank=True)


    def __str__(self):
        return f'{self.title.upper()} uploaded by {self.user.username if self.user else "Unknown"}'
    # class Meta:
    #     verbose_name_plural = 'Uploaded Books'

class ReadingProgress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    book_club = models.ForeignKey('bookclubs.BookClub', on_delete=models.CASCADE, null=True, blank=True)
    current_page = models.IntegerField(default=1)
    total_pages = models.IntegerField()
    last_read = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default = False)

    class Meta:
        unique_together = ['user', 'book', 'book_club']
    
    def __str__(self):
        return f'{self.user.username}--{self.book.title} ({self.current_page}/{self.total_pages})'
    
class Bookmark (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    page = models.IntegerField()
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.book.title} (Page {self.page})'
    

class ReadingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_sessions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_reading_sessions')  # Changed to Book model
    pages_read = models.IntegerField()
    minutes_spent = models.IntegerField()
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} read {self.pages_read} pages of {self.book.title} on {self.timestamp}'