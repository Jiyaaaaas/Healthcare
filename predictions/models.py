# predictions/models.py
from django.db import models
from django.contrib.auth.models import User

class HeartPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    sex = models.IntegerField()  # 1=Male, 0=Female
    chestpain = models.IntegerField()
    restingbp = models.FloatField()
    cholesterol = models.FloatField()
    fastingbs = models.IntegerField()
    maxhr = models.FloatField()
    exerciseangina = models.IntegerField()
    oldpeak = models.FloatField()
    st_slope = models.IntegerField()
    result = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class DiabetesPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pregnancies = models.IntegerField()
    glucose = models.FloatField()
    bp = models.FloatField()
    skin_thickness = models.FloatField()
    insulin = models.FloatField()
    bmi = models.FloatField()
    diabetes_pedigree = models.FloatField()
    age = models.IntegerField()
    result = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class MenstrualPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cycle_length = models.IntegerField()
    bleeding_days = models.IntegerField()
    pain_level = models.IntegerField()
    result = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)