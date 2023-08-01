from django.db import models
from time import strftime


class SecondOrdersModel(models.Model):
    serial_no = models.CharField(max_length=16)
    product_type = models.IntegerField()
    longitude = models.DecimalField(max_digits=45, decimal_places=20, blank=True, null=True)
    latitude = models.DecimalField(max_digits=45, decimal_places=20)
    height = models.IntegerField(blank=True, null=True)
    altitude = models.IntegerField(blank=True, null=True)
    phone_app_latitude = models.DecimalField(max_digits=45, decimal_places=20, blank=True, null=True)
    phone_app_longitude = models.DecimalField(max_digits=45, decimal_places=20, blank=True, null=True)
    phone_app_x = models.DecimalField(max_digits=45, decimal_places=20, blank=True, null=True)
    phone_app_y = models.DecimalField(max_digits=45, decimal_places=20, blank=True, null=True)
    home_latitude = models.DecimalField(max_digits=45, decimal_places=20, blank=True, null=True)
    home_longitude = models.DecimalField(max_digits=45, decimal_places=20, blank=True, null=True)
    home_x = models.DecimalField(max_digits=45, decimal_places=20, blank=True, null=True)
    home_y = models.DecimalField(max_digits=45, decimal_places=20, blank=True, null=True)
    dt = models.DateTimeField()
    frame_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return f"{self.serial_no} {self.product_type}, {self.longitude} {self.latitude} {self.height}" \
               f"{self.altitude} {self.phone_app_longitude} {self.phone_app_latitude} {self.home_latitude} {self.home_x} {self.home_y}" \
               f"{self.home_longitude} {self.dt} {self.frame_id} {self.status}"

    class Meta:
        verbose_name = 'SecondOrdersModel'
        verbose_name_plural = 'SecondOrdersModel'


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


class StatisticDataSet(models.Model):
    serial_no = models.CharField(max_length=255)
    dt = models.DateTimeField()
    product_type = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.serial_no} {self.dt} {self.product_type} {self.quantity}"

    class Meta:
        verbose_name = 'StatisticDataSet'
        verbose_name_plural = 'StatisticDataSet'


class FlightRecorderModel(models.Model):
    drone_type = models.CharField(max_length=50)
    record_data = models.DateTimeField()
    drone_id = models.CharField(max_length=255, null=True, blank=True)
    coord_x = models.CharField(max_length=100)
    coord_y = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.drone_type} {self.record_data} {self.drone_id} {self.coord_x} {self.coord_y}"

    class Meta:
        verbose_name = 'FlightRecorderModel'
        verbose_name_plural = 'FlightRecorderModel'
