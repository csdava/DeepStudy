from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import DiscussionPost, InteractionStatistics


@receiver(post_save, sender=User)
def create_user_stats(sender, instance, created, **kwargs):
    if created:
        InteractionStatistics.objects.create(user=instance)


@receiver(post_save, sender=DiscussionPost)
def update_stats_on_post_create(sender, instance, created, **kwargs):
    if created:
        stats, _ = InteractionStatistics.objects.get_or_create(user=instance.created_by)
        stats.post_count += 1
        stats.save()


@receiver(post_delete, sender=DiscussionPost)
def update_stats_on_post_delete(sender, instance, **kwargs):
    try:
        stats = InteractionStatistics.objects.get(user=instance.created_by)
        stats.post_count -= 1
        stats.save()
    except InteractionStatistics.DoesNotExist:
        pass 