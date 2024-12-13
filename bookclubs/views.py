from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import BookClub,Membership,Comment
from book.models import Book
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
    members = Membership.objects.filter(book_club=bookclub)
    return render(request, 'bookclubs/book_club_details.html', {'bookclub': bookclub, 'members':members,})

@login_required(login_url='login')
def book_club_list(request):
    # Filter book clubs created by the logged-in user
    book_clubs = BookClub.objects.filter(creator=request.user)
    my_book_clubs = BookClub.objects.filter(membership__user=request.user).exclude(creator=request.user).distinct()
    return render(request, 'bookclubs/book_club_list.html', {'book_clubs': book_clubs, 'my_book_clubs':my_book_clubs},)

@login_required(login_url='login')
def delete_book_club(request,id):
    bookclub = get_object_or_404(BookClub, id=id)
    try:
        bookclub.delete()
        messages.success(request,'Bookclub deleted successfully')
    except Exception as e:
        messages.error(request, f'Bookclub not deleted: str{e} ')
    return redirect('book_club_list')


def edit_book_club(request, id):

    return render(request, 'bookclubs/book_club_details.html')