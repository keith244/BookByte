from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from . forms import BookForm
from .models import Book
from django.contrib import messages
import fitz
from django.conf import settings
import os, ebooklib
import base64
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
# Create your views here.
User = get_user_model()

def index(request):
    try:
        books = Book.objects.filter(user=request.user)
        print(f'Found {books.count()} books')
        return render(request, 'book/index.html',{'books':books})
    except Exception as e:
        print(f'Error:{str(e)}')
        messages.error(request,'Error uploading books')
        return render(request,'book/index.html')
  


def ireader(request):
    return render (request, 'book/reader.html')

@login_required(login_url='login')
def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            messages.success(request, 'Book uploaded successfully!')
            return redirect('index')
        messages.error(request, f'Form errors: {form.errors}')
    else:
        form = BookForm()
    return render(request, 'book/upload.html', {'form': form})



@login_required(login_url='login')
def delete_book(request,id):
    book = get_object_or_404(Book, id=id)
    try:
        book.delete()
        messages.success(request,'Book deleted successfully')
    except Exception as e:
        messages.error(request, f'Book not deleted: str{e} ')
    return redirect('index')



def read_book(request,id):
    book = get_object_or_404(Book, id=id)
    file_ext = os.path.splitext(book.pdf_file.path)[1].lower()

    context = {
        'book': book,
    }
    try:
        if file_ext == '.pdf':
            doc = fitz.open(book.pdf_file.path)

            #first page
            page = doc[0]
            pix = page.get_pixmap()
            img_data = base64.b64encode(pix.tobytes()).decode('utf-8')

            # add pdf specific context
            context.update({
                'total_pages': len(doc),
                'current_page': 1,
                'page_image':img_data,
                'file_type':'pdf'
            })

            doc.close()
        
        elif file_ext in ['.epub','.txt']:
            with open (book.pdf_file.path, 'r',encoding = 'utf-8', errors = 'replace') as file:
                file_content = file.read()
            
            context.update ({
                'file_content': file_content,
                'file_type':'text',
            })
        
        else:
            messages.error(request,'Unsupported file type')
    
    except Exception as e:
        messages.error(request, f'Error reading file: {str(e)}')

    return render(request, 'book/reader.html', context)