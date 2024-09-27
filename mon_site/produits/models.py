from django.db import models
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import admin

class Produit(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    quantity = models.IntegerField() 

    def __str__(self):
        return self.titre
    
class Panier(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produits = models.ManyToManyField(Produit, blank=True)
    

