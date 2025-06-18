from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    es_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {'Admin' if self.es_admin else 'Usuario'}"