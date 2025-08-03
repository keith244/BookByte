# BookByte - Copyright (C) 2025 Keith Kk
# Licensed under GNU GPLv3. See LICENSE for details.

from django import forms
from . models import Book,Bookmark,ReadingProgress

class BookForm(forms.ModelForm): 
    class Meta:
        model = Book
        fields = ['title','author','pdf_file','cover_pic']