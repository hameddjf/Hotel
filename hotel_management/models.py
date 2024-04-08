from django.db import models


# Create your models here.

class AvailableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='avaliable')


class Room(models.Model):
    STATUS_CHOICES = (
        ('avaliable', 'Available'),
        ('reserved', 'Reserved')
    )

    name = models.CharField(max_length=100, verbose_name='نام')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    area = models.CharField(max_length=30, verbose_name='منطقه')
    beds = models.IntegerField(verbose_name='تعداد تخت')
    hotel_name = models.CharField(max_length=50, verbose_name='هتل')

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['-name'])
        ]

    def __str__(self):
        return self.name


# objects

    objects = models.Manager()
    Available = AvailableManager()
