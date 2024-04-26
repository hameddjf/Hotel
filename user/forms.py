from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Customer, User


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='تأیید رمز عبور', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone_number',
                  'password1', 'password2')
        help_texts = {
            'email': None,  # اینجا می‌توانید پیام‌های راهنمای اضافی اضافه کنید
        }

    def clean_email(self):
        # اعتبارسنجی ایمیل در اینجا
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('این ایمیل قبلاً ثبت شده است.')
        return email

    def clean_phone_number(self):
        # اعتبارسنجی شماره تلفن در اینجا
        phone_number = self.cleaned_data['phone_number']
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('این شماره تلفن قبلاً ثبت شده است.')
        return phone_number

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    '''
    فورم ویرایش پروفایل یوزر
    '''
    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone_number')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        # اطمینان حاصل کنید که کاربر فعلی می‌تواند ایمیل خود را حفظ کند
        if User.objects.filter(email=email).exclude(
                id=self.instance.id).exists():
            raise forms.ValidationError(
                'این ایمیل توسط کاربر دیگری استفاده شده است.')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        # اطمینان حاصل کنید که کاربر فعلی می‌تواند شماره تلفن خود را حفظ کند
        if User.objects.filter(phone_number=phone_number).exclude(
                id=self.instance.id).exists():
            raise forms.ValidationError(
                'این شماره تلفن توسط کاربر دیگری استفاده شده است.')
        return phone_number


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['address', 'city', 'country',
                  'national_code', 'preferences', 'special_requests']
        widgets = {
            'preferences': forms.Textarea(attrs={'rows': 4}),
            'special_requests': forms.Textarea(attrs={'rows': 4}),
        }
