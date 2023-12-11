from django.db import models
from django.utils import timezone
import uuid
# Create your models here.
class Share(models.Model):
    share_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sender_id = models.CharField("sender id",max_length=255)
    recipient_id = models.CharField("recipient id",max_length=255)
    file_id = models.CharField("file id", max_length=255)
    share_timestamp = models.DateTimeField("share timestamp",default=timezone.now)

    def save(self, *args, **kwargs):
        # Call the parent class's save method to perform the actual save operation
        super().save(*args, **kwargs)

        # Access the user ID after saving
        returned_share_id = self.share_id
        return str(returned_share_id)
    
    def __str__(self):
        return str(self.file_id)
    
    class Meta:
        verbose_name = "Share"
        verbose_name_plural = "Shares"