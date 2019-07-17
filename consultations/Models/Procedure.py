from django.db import models


class Procedure(models.Model):
    name = models.TextField(null=False)
    # price = models.DecimalField(null=False, max_digits=15, decimal_places=2, default=0)
    
    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            # 'price': self.price
        }
