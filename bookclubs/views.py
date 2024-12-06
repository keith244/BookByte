from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import BookClub,Membership,Comment
# Create your views here.
User = get_user_model()

@login_required(login_url='login')
def create_book_club(request):
    if request.method == 'POST':
        
        name = request.POST.get('name')
        description = request.POST.get('description')
        members = request.POST.getlist('members')

        book_club = BookClub.objects.create( 
            name = name, 
            description = description,
            creator = request.user
        )

        for member_id in members:
            member = User.objects.get(id=member_id)
            role = 'Member'
            if member.id == request.user.id:
                role = 'Admin'
            Membership.objects.create(user=member, book_club=book_club, role=role)
        
        messages.success(request, 'Book club created successfully!')
        return redirect('book_club_detail',book_club_id = book_club.id)
    
    users = User.objects.all()

    return render(request, 'bookclubs/create_book_club.html', {'users':users})

def book_club_detail(request, book_club_id):
    book_club = get_object_or_404(BookClub, id=book_club_id)
    members = Membership.objects.filter(book_club_id=book_club.id)
    return render(request, 'bookclubs/book_club_details.html', {'book_club': book_club, 'members':members})

@login_required(login_url='login')
def book_club_list(request):
    # Filter book clubs created by the logged-in user
    book_clubs = BookClub.objects.filter(creator=request.user)
    my_book_clubs = BookClub.objects.filter(membership__user=request.user)
    return render(request, 'bookclubs/book_club_list.html', {'book_clubs': book_clubs, 'my_book_clubs':my_book_clubs},)

