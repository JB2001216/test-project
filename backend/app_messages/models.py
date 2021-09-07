from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="outbox")
    to_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="inbox")
    title = models.CharField(max_length=250)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

