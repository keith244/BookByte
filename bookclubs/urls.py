from django.urls import path
from . import views
import uuid

urlpatterns = [
    # book club creation and listing
    path('', views.create_book_club, name='create_book_club'),
    path('bookclubs/', views.book_club_list, name='book_club_list'),
    
    # view/edit club
    path('bookclub/<int:book_club_id>/', views.book_club_detail, name='book_club_detail'),
    path('book_club/<int:book_club_id>/edit_book_club/',views.edit_book_club, name='edit_book_club'),
    path('delete_book_club/<int:id>/', views.delete_book_club, name='delete_book_club'),

    # member actions
    path('bookclub/<int:book_club_id>/add_members/', views.add_members, name='add_members'),
    path('bookclub/<int:book_club_id>/remove/<uuid:user_id>/', views.remove_member,name='remove_member' ),
    path('book_club/<int:book_club_id>/exit/<uuid:user_id>/', views.exit_book_club, name='exit_book_club'),

    # book actions
    path('bookclub/<int:book_club_id>/add_book/', views.add_book_to_club, name ='add_book_to_club'),
    path('book_club/<int:book_club_id>/read/<int:book_id>/', views.read_book_club_book, name ='read_book_club_book'),
    path('bookclub/<int:book_club_id>/delete_club_book/<uuid:user_id>/<int:book_id>/', views.delete_club_book, name ='delete_club_book'),
]
