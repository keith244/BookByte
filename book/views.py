# BookByte - Copyright (C) 2025 Keith Kk
# Licensed under GNU GPLv3. See LICENSE for details.

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from . forms import BookForm
from .models import Book,ReadingProgress, ReadingSession
from django.contrib import messages
import fitz
from django.conf import settings
import os, ebooklib
import base64
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import datetime
from .utils import get_reading_stats
from django.db.models import Sum
import json
from bookclubs.models import BookClub


# Create your views here.
User = get_user_model()

def index(request):
    try:
        stats = get_reading_stats(request.user)
        books = Book.objects.filter(user =request.user).exclude(
            id__in = ReadingProgress.objects.filter(user=request.user).values_list('book_id',flat=True)
        )
        continue_reading = ReadingProgress.objects.filter(
            user = request.user,
            completed = False,
        ).select_related('book')

        for progress in continue_reading:
            progress.persent_completed = ( # type: ignore
                (progress.current_page / progress.total_pages) * 100
                if progress.total_pages else 0
            )
        progress_count = ReadingProgress.objects.filter(
            user = request.user,
            completed = False
        ).count()

        return render(request, 'book/index.html',{
            'books':books,
            'continue_reading':continue_reading,
            'progress_count': progress_count,
            'stats':stats
            })
    except Book.DoesNotExist:
        messages.error(request,'No books found.')
        return render(request,'book/index.html',{'books':[],'continue_reading':[]})
    except AttributeError:
        messages.error(request, 'User authentication required')
        return render(request, 'book/index.html', {'books': [], 'continue_reading': []})
    except Exception as e:
        print(f'Error: {str(e)}')  # For debugging
        messages.error(request, f'Error: {str(e)}')
        return render(request, 'book/index.html', {'books': [], 'continue_reading': []})
  


# def ireader(request):
#     return render (request, 'book/reader.html')

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
    created = False

    book_club = None
    if 'book_club_id' in request.GET:
        book_club_id = request.GET.get('book_club_id')
        book_club = get_object_or_404(BookClub, id=book_club_id)

    
    # Try to get existing progress (individual first, then club)
    progress = None
    if book_club:
        try:
            progress = ReadingProgress.objects.get(user=request.user, book=book, book_club=book_club)
        except ReadingProgress.DoesNotExist:
            # Check if individual progress exists to copy from
            try:
                individual_progress = ReadingProgress.objects.get(user=request.user, book=book, book_club=None)
                progress = ReadingProgress.objects.create(
                    user=request.user,
                    book=book,
                    book_club=book_club,
                    current_page=individual_progress.current_page,
                    total_pages=individual_progress.total_pages,
                    completed=individual_progress.completed
                )
            except ReadingProgress.DoesNotExist:
                progress = ReadingProgress.objects.create(
                    user=request.user,
                    book=book,
                    book_club=book_club,
                    current_page=1,
                    total_pages=0
                )
    else:
        progress, created = ReadingProgress.objects.get_or_create(
            user=request.user,
            book=book,
            book_club=None,
            defaults={'current_page': 1, 'total_pages': 0}
        )
    # progress_percentage = (progress.current_page / progress.total_pages * 100)
    if created or not progress.completed:
        progress.completed = False
        progress.save()

    context = {
        'book': book,
        'current_page': progress.current_page,
        'completed': progress.completed,
    }

    try:
        if file_ext == '.pdf':
            doc = fitz.open(book.pdf_file.path)
            total_pages = len(doc)


            if progress.total_pages != total_pages:
                progress.total_pages = total_pages
                progress.save()


            page = doc[progress.current_page - 1]
            #first page
            # page = doc[0]
            pix = page.get_pixmap() # type: ignore
            img_data = base64.b64encode(pix.tobytes()).decode('utf-8')

            # add pdf specific context
            context.update({
                'total_pages': total_pages,#len(doc),
                # 'current_page': 1,
                'page_image':img_data,
                'file_type':'pdf',
                # 'progress_percentage': progress_percentage,
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
    request.session['start_page'] = progress.current_page
    request.session['start_time'] = str(datetime.datetime.now().timestamp())


    return render(request, 'book/reader.html', context)


# @login_required(login_url='login')
def book_reading_progress(request,id):

    if request.method == 'POST':

        # if request.user.is_authenticated:
        book = get_object_or_404(Book, id=id)

        book_club = None 
        if 'book_club_id' in request.GET:
            book_club_id = request.GET.get('book_club_id')
            book_club = get_object_or_404(BookClub, id=book_club_id)

        current_book = ReadingProgress.objects.get(
            book=book, 
            user=request.user,
            book_club=book_club,
        )            
        current_page = int(request.POST.get('current_page',current_book.current_page))       
        current_book.current_page = current_page  
        current_book.completed = current_page >= current_book.total_pages 
        start_page = request.session.get('start_page')
        start_time = request.session.get('start_time')

        if start_page and start_time:
            pages_read = current_page - int(start_page)
            minutes_spent = (datetime.datetime.now().timestamp() - float(start_time))/60
            minutes_spent = max(1, int(minutes_spent))
            if pages_read > 0:
                ReadingSession.objects.create(
                    user = request.user,
                    book = book,
                    pages_read = pages_read,
                    minutes_spent = minutes_spent,
                )
            request.session['start_page'] = current_page
            request.session['start_time'] = str(datetime.datetime.now().timestamp())
        print(current_book)
        current_book.save()

        return JsonResponse({'current_page':current_book.current_page,'success': True })
        
    return JsonResponse({'success':False},status=400)


@login_required(login_url='login')
def continue_reading_book(request):
    # Get books the user has started but not completed
    books_in_progress = ReadingProgress.objects.filter(
        user=request.user, 
        completed=False
    ).select_related('book')  # To avoid extra DB hits for books

    books = [progress.book for progress in books_in_progress]  # Extract book objects
    
    return render(request, 'book/index.html', {'books': books})


# tracking book reading sessions
# @login_required(login_url = 'login')
def save_reading_session(request, id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=id)
        pages_read = int(request.POST.get('pages_read',0))
        minutes_spent = int(request.POST.get('minutes_spent', 0))

        if pages_read > 0 and minutes_spent > 0:
            ReadingSession.objects.create(
                user = request.user,
                book = book,
                pages_read = pages_read,
                minutes_spent = minutes_spent,
            )
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid data'}, status = 400)


"view to display reading stats for user"
def reading_stats_view(request):
    """View for displaying reading statistics charts"""
    import json
    from django.db.models import Sum
    
    stats = get_reading_stats(request.user)
    
    # Get data for the weekly chart
    today = datetime.datetime.now().date()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    
    # Create data for each day of the current week
    weekly_data = []
    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    for i in range(7):
        current_date = start_of_week + datetime.timedelta(days=i)
        
        # Get total pages read for this specific day
        daily_pages = ReadingSession.objects.filter(
            user=request.user,
            timestamp=current_date
        ).aggregate(Sum('pages_read'))['pages_read__sum'] or 0
        
        weekly_data.append({
            'day': day_names[i],
            'date': current_date.strftime('%Y-%m-%d'),
            'pages': daily_pages
        })
    
    context = {
        'stats': stats,
        'weekly_data': json.dumps(weekly_data),
    }
    
    return render(request, 'book/reading_stats.html', context)