"""import pockets"""
from django.db import models


class SecondOrdersModel(models.Model):
    """Model for second online order page"""
    serial_no = models.CharField(max_length=16, default='unknown')
    product_type = models.IntegerField(default=0, null=True, blank=True)
    longitude = models.DecimalField(max_digits=45, decimal_places=20, blank=True, null=True)
    latitude = models.DecimalField(max_digits=45, decimal_places=20, blank=True, null=True)
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
        """return str data funct"""
        return f"{self.serial_no} {self.product_type}, {self.longitude} {self.latitude} {self.height}" \
               f"{self.altitude} {self.phone_app_longitude} {self.phone_app_latitude} {self.home_latitude} {self.home_x} {self.home_y}" \
               f"{self.home_longitude} {self.dt} {self.frame_id} {self.status}"

    class Meta:
        verbose_name = 'SecondOrdersModel'
        verbose_name_plural = 'SecondOrdersModel'


class CombatOrdersModel(models.Model):
    """model for auto collectins data in combat orders page """
    serial_no = models.CharField(max_length=255, default='unknown')
    dt = models.DateTimeField()
    product_type = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.IntegerField()
    status = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.serial_no} {self.dt} {self.product_type} {self.quantity} {self.status}"

    class Meta:
        verbose_name = 'CombatOrdersModel'
        verbose_name_plural = 'CombatOrdersModel'


# Create your models here.
class MainOrders(models.Model):
    """class for main page"""
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
    """class for collect statistics"""
    serial_no = models.CharField(max_length=255)
    dt = models.DateTimeField()
    product_type = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.serial_no} {self.dt} {self.product_type} {self.quantity}"

    class Meta:
        verbose_name = 'StatisticDataSet'
        verbose_name_plural = 'StatisticDataSet'


class DataForCombatLogic(models.Model):
    serial_no = models.CharField(max_length=100)
    dt = models.DateTimeField()
    product_type = models.CharField(max_length=25)
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.serial_no} {self.dt} {self.product_type} {self.quantity} {self.status}"

    class Meta:
        verbose_name = 'DataForCombatLogic'
        verbose_name_plural = 'DataForCombatLogic'


class FlightRecorderModel(models.Model):
    """model for fly recorder page"""
    drone_type = models.CharField(max_length=50)
    record_data = models.DateTimeField(auto_now=True)
    drone_id = models.CharField(max_length=255, null=True, blank=True)
    coord_x = models.CharField(max_length=100)
    coord_y = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.drone_type} {self.record_data} {self.drone_id} {self.coord_x} {self.coord_y}"

    class Meta:
        verbose_name = 'FlightRecorderModel'
        verbose_name_plural = 'FlightRecorderModel'


class SkySafeData(models.Model):
    """model for sky safe data page"""
    sensor_id = models.CharField(max_length=255, null=True, blank=True)
    station_id = models.CharField(max_length=255, null=True, blank=True)
    persistent_id = models.CharField(max_length=255, null=True, blank=True)
    tgt_model = models.CharField(max_length=255, null=True, blank=True)
    rc_id = models.CharField(max_length=255, null=True, blank=True)
    dl_freq = models.CharField(max_length=255, null=True, blank=True)
    dl_rssi = models.CharField(max_length=255, null=True, blank=True)
    ul_rssi = models.CharField(max_length=255, null=True, blank=True)
    home_position_lan = models.DecimalField(max_digits=45, decimal_places=20, null=True, blank=True)
    home_position_lon = models.DecimalField(max_digits=45, decimal_places=20, null=True, blank=True)
    app_position_lan = models.DecimalField(max_digits=45, decimal_places=20, null=True, blank=True)
    app_position_lon = models.DecimalField(max_digits=45, decimal_places=20, null=True, blank=True)
    tgt_position_lan = models.DecimalField(max_digits=45, decimal_places=20, null=True, blank=True)
    tgt_position_lon = models.DecimalField(max_digits=45, decimal_places=20, null=True, blank=True)
    tgt_alt_msl = models.CharField(max_length=255, null=True, blank=True)
    tgt_alt_hae = models.CharField(max_length=255, null=True, blank=True)
    tgt_alt_prs = models.CharField(max_length=255, null=True, blank=True)
    write_time = models.DateTimeField()

    def __str__(self):
        return f"{self.sensor_id} {self.station_id} {self.persistent_id} {self.tgt_model} {self.rc_id}" \
               f"{self.dl_freq} {self.dl_rssi} {self.ul_rssi} {self.home_position_lan} {self.home_position_lon}" \
               f"{self.app_position_lan} {self.app_position_lon}" \
               f"{self.tgt_position_lan} {self.tgt_position_lon} {self.tgt_alt_msl} {self.tgt_alt_hae}" \
               f" {self.tgt_alt_prs} {self.write_time}"

    class Meta:
        verbose_name = 'SkySafeData'
        verbose_name_plural = 'SkySafeData'
