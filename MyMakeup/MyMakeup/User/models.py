from django.db import models
from Admin.models import UserInfo,Product
from datetime import datetime
# Create your models here.

class MyCart(models.Model):
    user = models.ForeignKey(to='Admin.UserInfo', 
              on_delete=models.CASCADE)
    prdt = models.ForeignKey(to='Admin.Product', 
               on_delete=models.CASCADE)
    qty = models.IntegerField()

    class Meta:
        db_table  = "MyCart"

class MyOrder(models.Model):
    user = models.CharField(max_length = 20)
    pname = models.CharField(max_length=50)
    price = models.FloatField(default = 200)
    description = models.CharField(max_length=100)
    quantity = models.IntegerField()

    class Meta:
        db_table = "MyOrder"

class OrderMaster(models.Model):
    user = models.ForeignKey(to='Admin.UserInfo', 
              on_delete=models.CASCADE)
    amount = models.FloatField(default=1000)
    dateOfOrder = models.DateTimeField(default=datetime.now)
    details = models.CharField(max_length=200)
    class Meta:
        db_table  = "OrderMaster"

class Address(models.Model):
    address = models.CharField(max_length=500)
    landmark = models.CharField(max_length=500)
    state = models.CharField(max_length=520)
    pin = models.IntegerField()
    class Meta:
        db_table  = "Address"
