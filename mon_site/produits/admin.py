from django.contrib import admin
from .models import Produit

class ProduitAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'price', 'quantity')
    search_fields = ('titre',)
    list_filter = ('price',)
    ordering = ('-id',)

admin.site.register(Produit, ProduitAdmin)
   
