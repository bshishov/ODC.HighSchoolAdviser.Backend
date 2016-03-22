from django.db import models

# People who entered their email on launcher page
class Subscriber(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    ip = models.GenericIPAddressField() 

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural ="Подписчики"

    def __str__(self):
        return self.email


            