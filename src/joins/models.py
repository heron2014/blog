from django.db import models


class Join(models.Model):
    email = models.EmailField(unique=True)
    ip_address = models.CharField(max_length=120, default='ABC')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return str(self.email)
