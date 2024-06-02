from django.db import models


class TaxCode(models.Model):
    code = models.CharField(primary_key=True, max_length=100)
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.code
