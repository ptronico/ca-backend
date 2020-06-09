from django.db import models

from django.contrib.auth.models import User


class Review(models.Model):
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    summary = models.TextField(max_length=10000)
    rating = models.SmallIntegerField(default=5)
    ipv4 = models.GenericIPAddressField(protocol='IPv4')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.title}'
