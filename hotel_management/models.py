from django.db import models


# Create your models here.
class Room(models.Model):
    STATUS_CHOICES = (
        ('avaliable', 'Available'),
        ('reserved', 'Reserved')
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    area = models.CharField(max_length=30)
    beds = models.IntegerField()
    hotel_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
