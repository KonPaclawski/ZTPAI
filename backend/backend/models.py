from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255) 

class Budget(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    
class Payment(models.Model):
    id_budget = models.ForeignKey('Budget', on_delete=models.CASCADE)
    payment_title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    
