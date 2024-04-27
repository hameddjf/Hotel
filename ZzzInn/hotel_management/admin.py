from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Reservation, Room
# Register your models here.


class AvailableFilter(admin.SimpleListFilter):
    title = _('availability')
    parameter_name = 'availability'

    def lookups(self, request, model_admin):
        return (
            ('Yes', _('Available')),
            ('No', _('Not available')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(is_available=True)
        if self.value() == 'No':
            return queryset.filter(is_available=False)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'room_type', 'price', 'is_available')
    list_filter = ('room_type', AvailableFilter)
    search_fields = ('number', 'features')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        for room in queryset:
            if room.is_available:
                pass
        return queryset

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'room', 'check_in', 'check_out')
    list_filter = ('check_in', 'check_out')
    # اطمینان حاصل کنید که فیلد `name` در مدل `Customer` وجود دارد
    search_fields = ('customer__name', 'room__number')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
