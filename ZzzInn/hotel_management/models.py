from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.


class Reservation(models.Model):
    customer = models.ForeignKey(
        'user.Customer', verbose_name=_("مشتری"), on_delete=models.CASCADE)
    room = models.ForeignKey('Room', verbose_name=_(
        "اتاق"), on_delete=models.CASCADE)
    check_in = models.DateField(_("تاریخ ورود"))
    check_out = models.DateField(_("تاریخ خروج"))
    # سایر فیلدهای مربوط به رزرواسیون

    class Meta:
        verbose_name = _("رزرو اتاق")
        verbose_name_plural = _("رزرو اتاق‌ها")


class Room(models.Model):
    ROOM_TYPES = (
        ('single', _('تک نفره')),
        ('double', _('دو نفره')),
        ('suite', _('سوئیت')),
        # سایر انواع اتاق‌ها
    )
    room_type = models.CharField(
        _("نوع اتاق"), choices=ROOM_TYPES, max_length=50)
    number = models.CharField(_("شماره اتاق"), max_length=10, unique=True)
    price = models.DecimalField(_("قیمت"), max_digits=10, decimal_places=2)
    features = models.TextField(_("ویژگی‌ها"), blank=True)

    @property
    def is_available(self):
        # بررسی وجود رزرواسیون فعال برای این اتاق
        return not Reservation.objects.filter(
            room=self,
            check_out__gte=timezone.now()).exists()

    def __str__(self):
        occupancy_status = _("خالی") if self.is_available else _("اشغال")
        return f"Room {self.number} - {self.get_room_type_display()} \
            ({occupancy_status})"

    class Meta:
        verbose_name = _("اتاق")
        verbose_name_plural = _("اتاق‌ها")
