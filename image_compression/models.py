from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class CompressImage(models.Model):
    # [(10, 10), (20, 20), (30, 30), ..........]
    # [(value, label), (value, label), ........]
    QualityChoices = [(i, i) for i in range(10, 101, 10)]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_img = models.ImageField(upload_to='original_images/')
    quality = models.IntegerField(choices=QualityChoices, default=80)
    compressed_img = models.ImageField(upload_to='compressed_images/')
    compressed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username