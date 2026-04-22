from django.db import models

class Property(models.Model):
    PROPERTY_TYPES = [
        ('BOARDING_HOUSE', 'Boarding House'),
        ('APARTMENT', 'Apartment'),
        ('HOUSE', 'House'),
    ]
    
    name = models.CharField(max_length=200)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default='BOARDING_HOUSE')
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='property_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_occupied = models.BooleanField(default=False)
    image = models.ImageField(upload_to='room_photos/', blank=True, null=True)

    def __str__(self):
        if self.property:
            return f"{self.name} ({self.property.name})"
        return self.name