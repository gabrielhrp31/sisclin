from django.db import models
from .Address import Address


class Patient(models.Model):
    name = models.TextField(null=False, default="")
    gender = models.NullBooleanField(null=True)
    birth_date = models.DateField(null=True)
    email = models.EmailField(null=False)
    phone = models.TextField(null=False)
    RG = models.TextField(null=False)
    CPF = models.TextField(null=False)
    comments = models.TextField(null=True)
    found_us_by = models.TextField(null=True)
    address = models.ForeignKey(Address, on_delete=models.SET(None))
    
    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'name', self.name,
            'gender', self.gender,
            'birth_date', self.birth_date,
            'email', self.email,
            'phone', self.phone,
            'RG', self.RG,
            'CPF', self.CPF,
            'address', self.address.as_dict(),
        }
