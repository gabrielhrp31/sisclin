from django.db import models


class Address(models.Model):
    country = models.TextField(null=False)
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

    def is_valid(self):
        if not self.country or not self.street or not self.number or not self.city or not self.district:
            return False
        return (self.number > '0') and (not self.district.isspace()) and (self.street.replace(" ", "").isalnum() and not self.street.isspace()) and (self.country.isalnum() and not self.country.isspace()) and (self.city.replace(" ", "").isalnum() and not self.city.isspace())

    def get_full_address(self):
        return self.street+', '+str(self.number)+', '+self.district+' - '+self.city+'/'+self.country
