from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import BookClub,BookClubBook,Membership,Comment
from book.models import Book
from django.http import HttpResponseForbidden
# Create your views here.
User = get_user_model()

@login_required(login_url='login')
def create_book_club(request):
    if request.method == 'POST':
        
        name = request.POST.get('name')
        description = request.POST.get('description')
        members = request.POST.getlist('members')

        if not name or not description or not members:
            messages.error(request,f'All fields must be filled')
            return redirect ('create_book_club')
        

        try:
            bookclub = BookClub.objects.create( 
                name = name, 
                description = description,
                creator = request.user
            )
            # Ensures that the creator is added automatically as admin
            Membership.objects.create(user=request.user, book_club=bookclub, role='Admin')

            for member_id in members:
                if member_id != str (request.user.id):
                    member = User.objects.get(id=member_id)
                    Membership.objects.create (user=member, book_club=bookclub,role='Member')
                
            messages.success(request, 'Book club created successfully!')
            return redirect('book_club_detail',book_club_id = bookclub.id)
        except Exception as e:
            messages.error(request, f'All fields must be filled')
    
    users = User.objects.all()

    return render(request, 'bookclubs/create_book_club.html', {'users':users})

@login_required(login_url='login')
def book_club_detail(request,book_club_id):
    bookclub = get_object_or_404(BookClub, id=book_club_id)
    members = Membership.objects.filter(book_club=bookclub).select_related('user')
    
    is_admin = Membership.objects.filter(
        user = request.user,
        book_club = bookclub,
        role = 'Admin'
    ).exists()

    club_books = BookClubBook.objects.filter(
        book_club_id = book_club_id
    ).select_related('book','added_by')

    context = {
        'bookclub':bookclub,
        'members':members,
        'club_books': club_books,
        'is_admin':is_admin
    }

    return render(request, 'bookclubs/book_club_details.html', context)

@login_required(login_url='login')
def book_club_list(request):
    # Filter book clubs created by the logged-in user
    book_clubs = BookClub.objects.filter(creator=request.user)
    my_book_clubs = BookClub.objects.filter(membership__user=request.user).exclude(creator=request.user).distinct()
    return render(request, 'bookclubs/book_club_list.html', {'book_clubs': book_clubs, 'my_book_clubs':my_book_clubs},)

@login_required(login_url='login')
def add_members(request,book_club_id):
    book_club = get_object_or_404(BookClub, id=book_club_id)

    if request.method == 'POST' and request.user == book_club.creator:
        member_ids = request.POST.getlist('members')
        for user_id in member_ids:
            user = User.objects.get(id=user_id)
            if not book_club.members.filter(id=user.id).exists():
                Membership.objects.create(user=user,book_club=book_club)
            return redirect('book_club_detail', book_club_id = book_club_id)
    existing_members = book_club.members.all()
    available_users = User.objects.exclude(id__in=existing_members)

    return render(request,'bookclubs/book_club_details.html',{'bookclub':book_club, 'users':available_users})



@login_required(login_url='login')
def remove_member(request, book_club_id, user_id):
    book_club = get_object_or_404(BookClub, id=book_club_id)
    if request.user != book_club.creator:
        return HttpResponseForbidden()
    
    membership = get_object_or_404(Membership, book_club=book_club, user_id=user_id)
    if membership.user != book_club.creator:
        membership.delete()
    return redirect('book_club_detail', book_club_id=book_club_id)

@login_required(login_url='login')
def delete_book_club(request,id):
    bookclub = get_object_or_404(BookClub, id=id)
    try:
        bookclub.delete()
        messages.success(request,'Bookclub deleted successfully')
    except Exception as e:
        messages.error(request, f'Bookclub not deleted: str{e} ')
    return redirect('book_club_list')

@login_required(login_url='login')
def add_book_to_club (request, book_club_id):
    bookclub = get_object_or_404(BookClub, id=book_club_id)

    # check if user is admin
    if not Membership.objects.filter( user=request.user, book_club=bookclub, role = 'Admin' ).exists():
        messages.error (request, 'Only admins can add books')
        return redirect('book_club_detail', book_club_id=book_club_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        pdf_file = request.FILES.get('pdf_file')
        cover_pic = request.FILES.get('cover_pic')

        
        try:
            if not title and not author and not pdf_file:
                messages.error(request, 'Please fill all requested fields.')
                return redirect('add_book_to_club', book_club_id=book_club_id)
            
            book = Book.objects.create(
                user = request.user,
                title = title,
                author = author,
                pdf_file = pdf_file,
                cover_pic = cover_pic
            )
            BookClubBook.objects.create(
                book = book,
                book_club = bookclub,
                added_by = request.user
            )
            messages.success (request, 'Book added successfully to the club!')
            return redirect ('book_club_detail', book_club_id=book_club_id)
        except Exception as e:
            messages.error(request, f'Error adding book: {str(e)}')

    return render (request, 'bookclubs/add_book_to_club.html',{
        'bookclub': bookclub,
    })


@login_required(login_url='login')
def view_added_books(request, book_club_id = None):
    if book_club_id:
        books = BookClubBook.objects.filter(
        added_by = request.user,
        book_club_id = book_club_id,
    ).select_related('book', 'book_club')
        print(f'\n--- Books added by {request.user.username} to club ID {book_club_id}---')
    
    else:
        books = BookClubBook.objects.filter(
            added_by = request.user,
        ).select_related('book', 'book_club')
        print(f'\n All books added by {request.user.username}---')

    for book_entry in books:
        print(f"Title: {book_entry.book.title}")
        print(f"Author: {book_entry.book.author}")
        print(f"Club: {book_entry.book_club.name}")
        print(f"Added on: {book_entry.added_at}")
        print("-" * 40)
    
    # Return empty response or redirect
    return redirect('book_club_detail', book_club_id=book_club_id) if book_club_id else redirect('index')