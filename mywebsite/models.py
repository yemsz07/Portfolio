from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.
class myweb(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='web_images', null=False, blank=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f'{self.user.username} - {self.pub_date}'

    class Meta:
        ordering = ['-pub_date']