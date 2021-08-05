from django.db.models.signals import m2m_changed
from .models import Sale
from django.dispatch import receiver

@receiver(m2m_changed, sender=Sale.positions.through)
def calculate_total_price(sender, instance, action, **kwargs):
    total_price=0
    if(action =="post_add" or action =="post_remove"):
        for position in instance.get_postions():
            total_price += position.price
        instance.total_price=total_price
        instance.save()
