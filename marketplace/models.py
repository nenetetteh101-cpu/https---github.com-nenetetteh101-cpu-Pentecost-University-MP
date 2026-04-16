from django.db import models


# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.db import models
# from django.contrib.auth.models import User

# class Profile(models.py):
#     # This links the profile to a specific user
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
    
#     # Add unique fields here
#     bio = models.TextField(max_length=500, blank=True)
#     profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg')
#     location = models.CharField(max_length=100, blank=True)

#     def __str__(self):
#         return f'{self.user.username} Profile'
# # Create your models here.


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
