from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    class Meta:
        abstract = True
