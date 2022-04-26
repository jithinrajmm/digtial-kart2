from accounts.models import UserProfile

from accounts.models import Account

from django.dispatch import receiver

from django.db.models.signals import post_save


@receiver(post_save,sender=Account)
def profile_create_from_user(sender,instance,created,*args,**kwargs):
    if created:
        UserProfile.objects.create(user=instance,username=instance.username,first_name=instance.first_name,last_name=instance.last_name,email=instance.email,phone=instance.phone).save()

