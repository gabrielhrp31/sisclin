from django.db import models


class Address(models.Model):
    country = models.TextField(null=False)
    postal_code = models.TextField(null=False)
    city = models.TextField(null=False)
    street = models.TextField(null=False)
    number = models.IntegerField(null=False)

    def __str__(self):
        return self.street+', '+str(self.number)

    def as_dict(self):
        return {
            'id': self.id,
            'postal_code': self.postal_code,
            'country': self.country,
            'city': self.city,
            'street': self.street,
            'number': self.number
        }