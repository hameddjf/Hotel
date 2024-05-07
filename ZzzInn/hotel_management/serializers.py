from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from user.serializers import CustomerSerializer

from .models import Reservation, Room


class RoomSerializer(serializers.ModelSerializer):
    is_available = serializers.BooleanField(read_only=True)
    room_type_display = serializers.CharField(
        source='get_room_type_display', read_only=True
    )

    class Meta:
        model = Room
        fields = [
            'id', 'room_type', 'room_type_display',
            'number', 'price', 'features', 'is_available'
        ]


class ReservationSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        source='customer', queryset=Customer.objects.all(), write_only=True
    )
    room_id = serializers.primeryKeyRelatedField(
        source='room', queryset=Room.objects.all(), write_only=True
    )

    class Meta:
        model = Reservation
        fields = [
            'id', 'customer', 'customer_id', 'room', 'room_id',
            'check_in', 'check_out'
        ]

    def validate(self, data):
        """
        معتبرسازی‌های مربوط به تاریخ‌های ورود و خروج
        مثلا اطمینان حاصل کنید که تاریخ ورود قبل از تاریخ خروج است.
        """
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError(
                _("تاریخ ورود باید قبل از تاریخ خروج باشد."))
        return data
