from django.core.validators import MinValueValidator
from django.db import models

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, blank=True)
    model_name = models.CharField(max_length=200, blank=True)
    rental_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.model_name
