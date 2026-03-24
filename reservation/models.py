from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES = (
        ("admin","Admin"),
        ("staff","Staff"),
        ("customer","Customer"),
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default="customer")

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6,decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="images/",blank=False)

    def __str__(self):
        return self.name

class Table(models.Model):
    number = models.PositiveBigIntegerField(unique=True)
    seats = models.PositiveBigIntegerField()

    def __str__(self):
        return f"Table {self.number} - seats {self.seats}"
    
class Reservation(models.Model):
    STATUS = (
        ("pending","Pending"),
        ("confirmed","Confirmed"),
        ("cancelled","Cancelled")
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True,blank=True)
    table = models.ForeignKey(Table,on_delete=models.CASCADE)
    reservation_date = models.DateField()
    reservation_time = models.PositiveBigIntegerField()
    guests = models.PositiveBigIntegerField()
    status = models.CharField(max_length=10,choices=STATUS,default="pending")

    def __str__(self):
        return f"{self.user.username} - Table{self.table.number} on {self.reservation_date}"