from django.db import models
from django.conf import settings
from apps.books.models import Book

class Bookshelf(models.Model):
    STATUS_CHOICES = (
        ('to_read', 'To Read'),
        ('reading', 'Reading'),
        ('finished', 'Finished'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shelves')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='shelved_by')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to_read')
    pages_read = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=True)
    is_applied_to_explore = models.BooleanField(default=False)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
        verbose_name_plural = "Bookshelves"

    def save(self, *args, **kwargs):
        if not self.is_public:
            self.is_applied_to_explore = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s shelf: {self.book.title} ({self.get_status_display()})"

class BookCollection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='collections')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    books = models.ManyToManyField(Book, related_name='collections', blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s collection: {self.name}"

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

@receiver(post_save, sender=Bookshelf)
@receiver(post_delete, sender=Bookshelf)
def update_user_pages_read(sender, instance, **kwargs):
    user = instance.user
    stats = user.shelves.aggregate(
        total_pages=Sum('pages_read'),
    )
    total_pages = stats['total_pages'] or 0
    finished_books = user.shelves.filter(status='finished').count()
    
    # Points Logic: 
    # 1. 10 pts per finished book
    # 2. 10 pts per 100 pages (1 pt per 10 pages)
    points = (finished_books * 10) + (total_pages // 10)
    
    user.total_pages_read = total_pages
    user.points = points
    user.save(update_fields=['total_pages_read', 'points'])
