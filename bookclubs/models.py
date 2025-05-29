from django.db import models
from django.contrib.auth import get_user_model
from book.models import Book 

# Create your models here.
User = get_user_model()

class BookClub(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_clubs')
    members = models.ManyToManyField(User, related_name='book_clubs', through='Membership')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Name: {self.name} created by {self.creator.username}'
    
    class Meta:
        verbose_name_plural = 'Book Clubs'

class BookClubBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_club = models.ForeignKey(BookClub, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField (null = True, blank=True)
    end_date = models.DateField (null=True, blank=True)

    def __str__(self):
        return f"""Book Title: {self.book.title}  --- Club Name: {self.book_club.name}."""

    class Meta:
        unique_together = ['book', 'book_club']
        
class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_club = models.ForeignKey(BookClub, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=50,
        choices=[('Member','Member'),('Admin','Admin')],
        default='Member',
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}-- ({self.role})'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Coment by {self.user.username} on {self.book.title}'
    
    class Meta:
        verbose_name_plural = 'Comments'
