from django.contrib import admin
from django.urls import path
from produits import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('produit/<int:id>/', views.page_detail, name='page_detail'),
    path('about/', views.about, name='about'),
    path('base/', views.base, name='base'),
    path('listeProduits/', views.listeProduits, name='listeProduits'),
    path('search_results/', views.search_results, name='search_results'),
    path('panier/', views.panier, name='panier'),
    path('ajouter_au_panier/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('supprimer_produit/<int:produit_id>/', views.supprimer_produit, name='supprimer_produit'),
]
