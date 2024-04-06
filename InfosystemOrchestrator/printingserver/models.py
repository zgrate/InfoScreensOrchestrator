from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class StoredDocument(models.Model):
    DocumentPriorityChoice = [
        (1, "No Rush"),
        (2, "Need this tomorrow"),
        (3, "Need this in a few hours"),
        (4, "Need this in hour"),
        (5, "ASAP")
    ]
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.IntegerField(choices=DocumentPriorityChoice)
    description = models.CharField(max_length=255)
    delivery_location = models.CharField(max_length=255)
    number_of_pages = models.IntegerField()

    printed_at = models.DateTimeField(null=True, blank=True)

    file_to_print = models.FileField()

    @property
    def is_printed(self):
        return bool(self.printed_at is not None)

    def __str__(self):
        return f"Document: {self.description} from {self.user.username}"

