from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, full_name: str,
                    phone_number: str, password: str = None,
                    **extra_fields) -> 'User':
        # اعتبارسنجی ایمیل
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError('شما باید یک آدرس ایمیل معتبر ارائه دهید.')

        if not full_name:
            raise ValueError('نام کامل داده شده باید تنظیم شود.')
        if not phone_number:
            raise ValueError('شماره تلفن داده شده باید تنظیم شود.')

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name,
                          phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, full_name: str,
                         phone_number: str, password: str, username):
        user = self.create_user(
            email=self.normalize_email(email),
            full_name=full_name,
            username=username,
            phone_number=phone_number,
            password=password,
        )
        # giving permission to super user
        user.is_active = True
        user.is_staff = True
        user.is_admin = False
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    # personality
    full_name = models.CharField(_("نام و نام خانوادگی"), max_length=50)

    # communicational
    email = models.EmailField(_("ایمیل"), max_length=50, unique=True)
    phone_number = models.CharField(
        _('شماره تماس'), max_length=15, unique=True)

    # required
    date_joined = models.DateTimeField(
        _("زمان ثبت نام"), auto_now=False, auto_now_add=True)
    last_login = models.DateTimeField(
        _("اخرین ورود"), auto_now=False, auto_now_add=True)

    # فیلدهای مربوط به وضعیت کاربر
    is_admin = models.BooleanField(
        _("کاربر مورد نظر ادمین است؟"), default=False)
    is_staff = models.BooleanField(
        _("کاربر مورد نظر کارمند است؟"), default=False)
    is_active = models.BooleanField(
        _("کاربر مورد نظر فعال است؟"), default=True)
    is_superadmin = models.BooleanField(
        _("کاربر مورد نظر سوپرادمین است؟"), default=False)

    # برای ورود به سیستم از فیلد ایمیل استفاده می‌شود
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'phone_number']
    objects = CustomUserManager()

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin


SATISFACTION_LEVEL_CHOICES = [
    (1, 'بسیار ناراضی'), (2, 'ناراضی'),
    (3, 'معمولی'), (4, 'راضی'), (5, 'بسیار راضی')
]

RESERVATION_STATUS_CHOICES = [
    ('reserved', _("رزرو شده")),
    ('checked_in', _("وارد شده")),
    ('checked_out', _("خارج شده")),
    ('cancelled', _("لغو شده")),
]

PAYMENT_STATUS_CHOICES = [
    ('PAID', _('پرداخت شده')),
    ('PENDING', _('در انتظار')),
    ('FAILED', _('ناموفق')),
]


class Customer(models.Model):
    # personality
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("مشتری"))
    address = models.CharField(_("ادرس"), max_length=255, blank=True)
    city = models.CharField(_("شهر"), max_length=50, blank=True)
    country = models.CharField(_("کشور"), max_length=50, blank=True)
    check_in = models.DateField(_("تاریخ ورود"))
    check_out = models.DateField(_("تاریخ خروج"))
    guests_number = models.PositiveIntegerField(_("تعداد مهمان‌ها"))
    national_code = models.IntegerField(
        _("کد ملی"), unique=True)

    # service
    loyalty_points = models.IntegerField(_("امتیازات وفاداری"), default=0)
    preferences = models.TextField(_("ترجیحات اتاق"), blank=True)
    satisfaction_level = models.IntegerField(
        _("میزان رضایت"), null=True, blank=True,
        choices=SATISFACTION_LEVEL_CHOICES,
    )
    special_requests = models.TextField(_("درخواست‌های ویژه"), blank=True)
    reservation_status = models.CharField(
        _("وضعیت رزرو"), max_length=50,
        choices=RESERVATION_STATUS_CHOICES)
    payment_status = models.CharField(
        _("وضعیت پرداخت"), max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
    )
    room_number = models.CharField(_("شماره اتاق"), max_length=10, blank=True)

    # special
    special_requests = models.TextField(blank=True)  # درخواست‌های ویژه
    vip_status = models.BooleanField(default=False)  # وضعیت VIP بودن مشتری

    class Meta:
        verbose_name = _("رزرو")
        verbose_name_plural = _("رزروها")

    @property
    def is_active(self):
        return self.user.is_active

    @property
    def duration(self):
        return (self.check_out - self.check_in).days

    def __str__(self):
        return self.user.full_name


class HotelStaff(models.Model):
    # personality
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("کارمند"))
    address = models.CharField(_("آدرس"), max_length=255, blank=False)

    # job information
    role = models.CharField(_("وظیفه"), max_length=50)
    working_hours = models.IntegerField(_("ساعات کاری"))
    start_date = models.DateField(
        _("تاریخ شروع به کار"), null=True, blank=True)
    department = models.CharField(_("بخش"), max_length=50, blank=True)

    # Other necessary information
    emergency_contact = models.CharField(
        _("تماس اضطراری"), max_length=255, blank=True)
    salary = models.DecimalField(
        _("حقوق"), max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.user.full_name

    class Meta:
        permissions = (
            ("can_view", _("می‌تواند مشاهده کند")),
            ("can_edit", _("می‌تواند ویرایش کند")),
            ("can_delete", _("می‌تواند حذف کند")),
        )
        verbose_name = _("کارمند هتل")
        verbose_name_plural = _("کارمندان هتل")


class HotelAdmin(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("مدیر"))

    # اطلاعات مربوط به مدیریت
    department = models.CharField(_("بخش"), max_length=50, blank=True)
    start_date = models.DateField(
        _("تاریخ شروع به کار"), null=True, blank=True)
    permissions_level = models.CharField(
        _("سطح دسترسی"), max_length=50, default="Full")

    # توانایی‌های مدیریتی
    can_approve_transactions = models.BooleanField(
        _("تایید تراکنش‌ها"), default=False)
    can_modify_policies = models.BooleanField(
        _("تغییر خط‌مشی‌ها"), default=False)
    can_handle_complaints = models.BooleanField(
        _("رسیدگی به شکایات"), default=False)

    # اطلاعات تکمیلی
    biography = models.TextField(
        _("بیوگرافی"), blank=True, null=True)
    advanced_training_completed = models.BooleanField(
        _("تکمیل دوره‌های آموزشی پیشرفته"), default=False)

    def __str__(self):
        return self.user.full_name

    class Meta:
        permissions = (
            ("can_manage_staff",
             _("می‌تواند کارکنان را مدیریت کند")),
            ("can_change_hotel_settings",
             _("می‌تواند تنظیمات هتل را تغییر دهد")),
            ("can_view_financial_reports",
             _("می‌تواند گزارش‌های مالی را مشاهده کند")),
        )
        verbose_name = _("مدیر هتل")
        verbose_name_plural = _("مدیران هتل")
