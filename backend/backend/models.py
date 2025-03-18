from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)

class Budget(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    payment_title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
