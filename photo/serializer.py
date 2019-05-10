from rest_framework import serializers
from .models import ShipPhoto

class ShipPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShipPhoto
        fields = ('运单号tracking','照片photo','车牌carplates','发货名细xlsx','订单order','id')
