from django.db import models
from django.contrib.auth.models import User


class ProfileModel(models.Model):
    GENDER_TYPE = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        related_name='user_profile'
    )
    gender = models.CharField(
        choices=GENDER_TYPE, 
        max_length=20, 
        null=True
    )
    name = models.CharField(max_length=200, null=True) 
    gender = models.CharField(
        choices=GENDER_TYPE, 
        max_length=20, 
        null=True
    )  
    age = models.IntegerField(null=True)  
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    bmi = models.FloatField(null=True)
    bmr = models.FloatField(null=True)
    image = models.ImageField(upload_to='profile/', null=True, blank=True)

    def __str__(self):
        return f'{self.name}'
    
class CalorieConsume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_calorie')
    item_name = models.CharField(max_length=200, null=True)
    calorie_consumed = models.CharField(max_length=200, null=True)
    created_at = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.item_name}'
    
    