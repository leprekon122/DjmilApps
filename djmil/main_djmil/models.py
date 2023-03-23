from django.db import models


# Create your models here.
class MainOrders(models.Model):
    serial_no = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255)
    dt_first = models.DateTimeField(null=True, blank=True)
    dt_last = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.serial_no} {self.product_type} {self.dt_first} {self.dt_last}"

    class Meta:
        verbose_name = 'MainOrders'
        verbose_name_plural = 'MainOrders'
