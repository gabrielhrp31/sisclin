from django.db import models


class Address(models.Model):
    postal_code = models.TextField(null=False)
    city = models.TextField(null=False)
    country = models.TextField(null=False)
    street = models.TextField(null=False)
    number = models.IntegerField(null=False)

    def __str__(self):
        return self.street+', '+str(self.number)
