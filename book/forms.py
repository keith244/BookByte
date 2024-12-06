from django import forms
from . models import Book,Bookmark,ReadingProgress

class BookForm(forms.ModelForm): 
    class Meta:
        model = Book
        fields = ['title','author','pdf_file','cover_pic']