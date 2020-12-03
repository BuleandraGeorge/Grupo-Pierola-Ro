from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import orderLineItem


@receiver(post_save, sender=orderLineItem)
def update_on_save(sender, instance, created, **kwards):
    instance.order.update_total()


@receiver(post_delete, sender=orderLineItem)
def update_on_delete(sender, instance, **kwards):
    instance.order.update_total()
