
from django.db import models
from django.contrib.auth.models import User

class Listing(models.Model):
    # Linking the listing to the user who created it
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Core Data
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=50) # 'Products' or 'Services'
    condition = models.CharField(max_length=50, blank=True)
    
    # The Cloudinary URL string
    image_url = models.URLField(max_length=500) 
    
    # Status and Metadata
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"