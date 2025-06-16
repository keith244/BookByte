from django.utils import timezone
from django.db.models import Sum
from .models import ReadingSession, ReadingProgress

def get_reading_stats(user):
    today = timezone.now().date()
    start_of_week = today - timezone.timedelta(days=today.weekday())
    
    pages_today = ReadingSession.objects.filter(
        user=user,
        timestamp__year=today.year,
        timestamp__month=today.month,
        timestamp__day=today.day,
    ).aggregate(total=Sum('pages_read'))['total'] or 0
    
    pages_week = ReadingSession.objects.filter(
        user=user,
        timestamp__gte=start_of_week,
    ).aggregate(total=Sum('pages_read'))['total'] or 0
    
    last_session = ReadingSession.objects.filter(
        user=user
    ).order_by('-timestamp').first()
    
    last_book_title = last_session.book.title if last_session else "No reading activity"
    
    total_minutes = ReadingSession.objects.filter(
        user=user
    ).aggregate(total=Sum('minutes_spent'))['total'] or 0
    
    total_hours = round(total_minutes / 60, 2)

    completed_books_count = ReadingProgress.objects.filter(
        user=user,
        completed= True
    ).count()
    
    return {
        'pages_today': pages_today,
        'pages_week': pages_week,
        'last_book_title': last_book_title,
        'total_hours': total_hours,
        'completed_books_count':completed_books_count,
    }