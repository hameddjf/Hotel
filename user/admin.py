from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User, Customer, HotelStaff, HotelAdmin
# Register your models here.


@admin.register(User)
class UserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('full_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
         'is_admin', 'is_superadmin', 'groups', 'user_permissions')}),
        # حذف 'date_joined' از 'fieldsets' زیرا غیرقابل ویرایش است
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone_number',
                       'password1', 'password2',
                       'is_active', 'is_staff', 'is_admin'),
        }),
    )

    list_display = ('email', 'full_name', 'phone_number',
                    'is_staff', 'is_active', 'is_admin')
    search_fields = ('email', 'full_name', 'phone_number')
    ordering = ('email',)

    def save_model(self, request, obj, form, change):
        if 'password1' in form.cleaned_data \
                and 'password2' in form.cleaned_data:
            if form.cleaned_data['password1'] \
                    == form.cleaned_data['password2']:
                obj.set_password(form.cleaned_data['password1'])
        obj.save()

    readonly_fields = ('last_login', 'date_joined',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'check_in', 'check_out',
        'national_code',
        'loyalty_points', 'satisfaction_level',
        'reservation_status', 'payment_status', 'vip_status'
    )
    list_filter = (
        'city', 'country', 'satisfaction_level', 'reservation_status',
        'payment_status', 'vip_status'
    )
    search_fields = ('user__email', 'user__full_name',
                     'address', 'city', 'country', 'national_code')
    readonly_fields = ('is_active', 'duration')

    def full_name(self, obj):
        return obj.user.full_name
    full_name.short_description = _("نام کامل")

    fieldsets = (
        (_('Personal Information'), {
            'fields': ('user', 'address', 'city', 'country')
        }),
        (_('Reservation Details'), {
            'fields': ('check_in', 'check_out',
                       'guests_number', 'national_code')
        }),
        (_('Service Information'), {
            'fields': ('loyalty_points', 'preferences',
                       'satisfaction_level', 'special_requests')
        }),
        (_('Status'), {
            'fields': ('reservation_status', 'payment_status', 'vip_status')
        }),
        (_('Room Information'), {
            'fields': ('room_number',)
        }),
    )

    readonly_fields = ('is_active', 'duration')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HotelStaff)
class HotelStaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department',
                    'working_hours', 'start_date', 'salary')
    search_fields = ('user__username', 'user__first_name',
                     'user__last_name', 'role', 'department')
    list_filter = ('department', 'role')
    date_hierarchy = 'start_date'
    ordering = ('start_date',)
    fieldsets = (
        (_('Personal info'), {
         'fields': ('user', 'address', 'emergency_contact')}),
        (_('Job details'), {
         'fields': ('role', 'working_hours', 'start_date',
                    'department', 'salary')}),
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HotelAdmin)
class HotelAdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'start_date', 'permissions_level')
    search_fields = ('user__username', 'user__first_name',
                     'user__last_name', 'department')
    list_filter = ('department', 'permissions_level')
    date_hierarchy = 'start_date'
    ordering = ('start_date',)
    fieldsets = (
        (_('Management info'), {
         'fields': ('user', 'department', 'start_date', 'permissions_level')}),
        (_('Management abilities'), {'fields': (
            'can_approve_transactions', 'can_modify_policies',
            'can_handle_complaints')}),
        (_('Additional info'), {
         'fields': ('biography', 'advanced_training_completed')}),
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
