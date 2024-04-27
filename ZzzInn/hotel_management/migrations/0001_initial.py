# Generated by Django 5.0.3 on 2024-04-25 08:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0003_alter_hoteladmin_options_alter_hotelstaff_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(choices=[('single', 'تک نفره'), ('double', 'دو نفره'), ('suite', 'سوئیت')], max_length=50, verbose_name='نوع اتاق')),
                ('number', models.CharField(max_length=10, unique=True, verbose_name='شماره اتاق')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='قیمت')),
                ('features', models.TextField(blank=True, verbose_name='ویژگی\u200cها')),
            ],
            options={
                'verbose_name': 'اتاق',
                'verbose_name_plural': 'اتاق\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateField(verbose_name='تاریخ ورود')),
                ('check_out', models.DateField(verbose_name='تاریخ خروج')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.customer', verbose_name='مشتری')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel_management.room', verbose_name='اتاق')),
            ],
        ),
    ]
