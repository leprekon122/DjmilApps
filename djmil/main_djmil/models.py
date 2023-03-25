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


class SecondOrdersModel(models.Model):
    serial_no = models.CharField(max_length=16)
    product_type = models.IntegerField()
    longitude = models.DecimalField(max_digits=45, decimal_places=20, blank=True, null=True)
    latitude = models.DecimalField(max_digits=45, decimal_places=20)
    height = models.IntegerField( blank=True, null=True)
    altitude = models.IntegerField(blank=True, null=True)
    phone_app_latitude = models.DecimalField(max_digits=45, decimal_places=20, blank=True, null=True)
    phone_app_longitude = models.DecimalField(max_digits=45, decimal_places=20, blank=True, null=True)
    home_latitude = models.DecimalField(max_digits=45, decimal_places=20, blank=True, null=True)
    home_longitude = models.DecimalField(max_digits=45, decimal_places=20, blank=True, null=True)
    dt = models.DateTimeField()
    frame_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.serial_no} {self.product_type}, {self.longitude} {self.latitude} {self.height}" \
               f"{self.altitude} {self.phone_app_longitude} {self.phone_app_latitude} {self.home_latitude}" \
               f"{self.home_longitude} {self.dt} {self.frame_id}"

    class Meta:
        verbose_name = 'SecondOrdersModel'
        verbose_name_plural = 'SecondOrdersModel'
