from django.db import models


class Address(models.Model):
    country = models.TextField(null=False)
    postal_code = models.TextField(null=False)
    city = models.TextField(null=False)
    street = models.TextField(null=False)
    number = models.IntegerField(null=False)
    district = models.TextField(null=False, default='Insira um Bairro')

    def __str__(self):
        return self.street+', '+str(self.number)

    def as_dict(self):
        return {
            'id': self.id,
            'country': self.country,
            'city': self.city,
            'district': self.district,
            'street': self.street,
            'number': self.number
        }