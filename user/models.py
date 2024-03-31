from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    STATUS_CHOICES = (
        ('avaliable', 'Available'),
        ('reserved', 'Reserved')
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    area = models.CharField(max_length=30)
    beds = models.IntegerField(max_length=5)
    hotel = models.ForeignKey('Hotel', related_name='rooms', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Hotel(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='hotel_images/')

    def __str__(self):
        return self.name
