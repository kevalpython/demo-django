from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Book(models.Model):
    author = models.CharField(max_length=255, blank=True, null=True)
    book = models.CharField(max_length=255, blank=False, null=False)


class Notification(models.Model):
    """
    Django model class representing the notification details for a user.

    Attributes:
        user (ForeignKey): A foreign key to the `CustomUser` model, representing the user who will receive the notification.
        notification_title (str): The title of the notification.
        notification_description (str): A longer description of the notification.
        notification_body (JSONField): A JSON-encoded dictionary containing the notification body. This field can be used to store additional information related to the notification.
        notification_sent_at (DateTimeField): The datetime when the notification was sent.
        is_read (bool): A boolean field indicating whether the notification has been read by the user.

    Meta:
        verbose_name (str): A human-readable name for the model class in singular form.
        verbose_name_plural (str): A human-readable name for the model class in plural form.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    body = models.JSONField(blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "NotificationDetail"
        verbose_name_plural = "NotificationDetails"

    def __str__(self):
        """
        Returns a string representation of the Notification Details.
        """
        return f"{self.user}"
