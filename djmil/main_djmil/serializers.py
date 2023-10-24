"""import pockets"""
from rest_framework.serializers import ModelSerializer
from .models import SecondOrdersModel


class SecondOnlineOrderSerializer(ModelSerializer):
    """Serializer for SecondOrdersModel"""
    class Meta:
        model = SecondOrdersModel
        fields = ['serial_no', 'product_type', 'longitude', 'latitude', 'height', 'altitude',
                  'phone_app_latitude', 'phone_app_longitude', 'phone_app_x', 'phone_app_y',
                  'home_latitude', 'home_longitude', 'home_x', 'home_y', 'dt', 'frame_id', 'status']