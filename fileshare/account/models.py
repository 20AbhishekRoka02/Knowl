from django.db import models
import uuid
# Create your models here.
class User(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user_name = models.CharField("user name",max_length=255,default="user")
    email = models.EmailField("user email")
    phone = models.CharField("phone number",max_length=10,default=None, null=True)
    password = models.CharField("password", max_length=255,default=None, null=True)
    is_admin = models.BooleanField("is admin", default=False)
    
    def save(self, *args, **kwargs):
        # Call the parent class's save method to perform the actual save operation
        super().save(*args, **kwargs)

        # Access the user ID after saving
        user_id = self.id
        return str(user_id)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
    


