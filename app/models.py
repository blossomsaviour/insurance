from django.db import models
from django.urls import reverse


# Create your models here.)
class vehicle(models.Model):
    full_name = models.CharField(max_length=30)
    vehicle_name = models.CharField(max_length=30)
    vehicle_number = models.CharField(max_length=30)
    vehicle_reg_year = models.DateField()
    vehicle_price = models.IntegerField()
    insurance_name=models.CharField(max_length=30)
    insurance_type=models.IntegerField()
    insurance_price=models.IntegerField(default=0)

    def __str__(self):
        return self.vehicle_name

    def get_absolute_url(self):
        return reverse("vehicle_details", kwargs={"pk": self.pk})


class insurance(models.Model):
    insurance_name = models.CharField(max_length=30)
    insurance_basic_price = models.IntegerField()
    insurance_type = models.IntegerField()
    insurance_desc = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.insurance_name

    def get_absolute_url(self):
        return reverse("insurance_details", kwargs={"pk": self.pk})


class orders(models.Model):
    orderid=models.CharField(max_length=30)
    insurance_name=models.CharField(max_length=30)
    price=models.IntegerField()
    username=models.CharField(max_length=30)

    def __str__(self):
        return self.insurance_name

    def get_absolute_url(self):
        return reverse("insurance_details", kwargs={"pk": self.pk})
