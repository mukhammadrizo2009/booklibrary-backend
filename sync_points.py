import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.books.models import Book, Review

User = get_user_model()

def sync_points():
    users = User.objects.all()
    for user in users:
        book_points = user.added_books.count() * 5
        review_points = user.reviews.count() * 2
        total_points = book_points + review_points
        
        if user.points != total_points:
            print(f"Updating {user.username}: {user.points} -> {total_points}")
            user.points = total_points
            user.save(update_fields=['points'])
    print("Points sync completed.")

if __name__ == "__main__":
    sync_points()
