from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book, Review

@receiver(post_save, sender=Book)
def award_points_for_book(sender, instance, created, **kwargs):
    if created and instance.added_by:
        user = instance.added_by
        user.points += 5
        user.save(update_fields=['points'])

@receiver(post_save, sender=Review)
def award_points_for_review(sender, instance, created, **kwargs):
    if created and instance.user:
        user = instance.user
        user.points += 2
        user.save(update_fields=['points'])
