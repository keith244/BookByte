from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_book_club, name='create_book_club'),
    path('bookclubs/', views.book_club_list, name='book_club_list'),
    path('bookclub/<int:book_club_id>/', views.book_club_detail, name='book_club_detail'),
    path('delete_book_club/<int:id>/', views.delete_book_club, name='delete_book_club'),
    path('bookclub/<int:book_club_id>/remove/<uuid:user_id>/', views.remove_member,name='remove_member' ),
    path('bookclub/<int:book_club_id>/add_members/', views.add_members, name='add_members'),
    path('bookclub/<int:book_club_id>/add_book/', views.add_book_to_club, name ='add_book_to_club'),
]
