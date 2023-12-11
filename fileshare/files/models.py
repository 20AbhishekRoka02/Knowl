# from collections.abc import Iterable
from django.db import models
from django.utils import timezone
import uuid

# Create your models here.
class File(models.Model):
    file_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user_id = models.CharField("user id", max_length=255)
    size = models.FloatField("size")
    file_name = models.CharField("file name", max_length=255)
    upload_date = models.DateTimeField("Upload Date",default=timezone.now)
    upload_file = models.FileField(upload_to='uploads/')

    def save(self, *args, **kwargs):
        # Call the parent class's save method to perform the actual save operation
        super().save(*args, **kwargs)

        # Access the user ID after saving
        returned_file_id = self.file_id
        return str(returned_file_id)
    
    def __str__(self):
        return str(self.file_id)
    
    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"
