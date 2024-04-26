from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):
    """
    یک فورم برای ایجاد و ویرایش رزرواسیون اتاق.
    """
    class Meta:
        model = Reservation
        fields = ['customer', 'room', 'check_in', 'check_out', 'guests_number',
                  'reservation_status', 'payment_status', 'special_requests']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
