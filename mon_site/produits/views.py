from django.shortcuts import render, get_object_or_404, redirect
from .models import Produit, Panier
from django.conf import settings
import stripe
from django.http import JsonResponse

def ajouter_au_panier(request, produit_id):
   
    panier = request.session.get('panier', {})

    if str(produit_id) in panier:
        panier[str(produit_id)] += 1
    else:
        panier[str(produit_id)] = 1

    request.session['panier'] = panier
    
    # Incrémenter le nombre d'articles dans le panier
    if 'cart_count' not in request.session:
        request.session['cart_count'] = 0
    request.session['cart_count'] += 1
    request.session.modified = True
    
    return redirect('listeProduits')

def index(request):
    if 'cart_count' not in request.session:
        request.session['cart_count'] = 0
    return render(request, 'index.html')

def page_detail(request, id):
    produit = get_object_or_404(Produit, id=id)
    return render(request, 'page_detail.html', {'produit': produit})

def about(request):
    return render(request, 'about.html')

def base(request):
    return render(request, 'base.html')

def listeProduits(request):
    produits = Produit.objects.all()
    return render(request, 'listeProduits.html', {'produits': produits})

def search_results(request):
    query = request.GET.get('query')
    if query:
        produits = Produit.objects.filter(titre__icontains=query)
    else:
        produits = Produit.objects.all()
    return render(request, 'search_results.html', {'produits': produits, 'query': query})

def panier(request):
    produits = []
    quantite = {}
    total_price = 0.0  
    stripe.api_key = settings.STRIPE_PUBLIC_KEY

    if request.user.is_authenticated:
        panier = Panier.objects.filter(user=request.user).first()
        if panier:
            produits = panier.produits.all()
            quantite = {str(produit.id): 1 for produit in produits}  # Utiliser 1 si la quantité n'est pas stockée
            total_price = sum(float(produit.price) * quantite[str(produit.id)] for produit in produits)
    else:
        panier = request.session.get('panier', {})
        produits_ids = list(map(int, panier.keys()))  # Convertir les IDs en entiers
        produits = Produit.objects.filter(id__in=produits_ids)
        
        # Calculer les quantités et les prix totaux
        quantite = {str(produit.id): int(panier.get(str(produit.id), 0)) for produit in produits}
        total_price = sum(float(produit.price) * quantite[str(produit.id)] for produit in produits)
        total_price_stripe = total_price*100
        
    prixTotalParProduit = []
    for produit in produits:
        produit.quantite = quantite[str(produit.id)]
        produit.prix_total = produit.price * produit.quantite
        prixTotalParProduit.append(produit)

    return render(request, 'panier.html', {
        'produits': prixTotalParProduit,
        'total_price': total_price,
        'total_price_stripe':total_price_stripe,
        'key': settings.STRIPE_PUBLIC_KEY
    })

def supprimer_produit(request, produit_id):
    panier = request.session.get('panier', {})
    produit_id_str = str(produit_id)
    
    if produit_id_str in panier:
        if panier[produit_id_str] > 1:
            panier[produit_id_str] -= 1
        else:
            del panier[produit_id_str]
        
        # Mettre à jour le compteur du panier
        request.session['cart_count'] = sum(panier.values())
        request.session['panier'] = panier
    
    return redirect('panier')


def add_to_cart(request, produit_id):
    panier = request.session.get('panier', {})

    if str(produit_id) in panier:
        panier[str(produit_id)] += 1
    else:
        panier[str(produit_id)] = 1

    # Mettre à jour le compteur du panier
    request.session['cart_count'] = sum(panier.values())
    request.session['panier'] = panier

    # Rediriger vers la page des produits ou toute autre page
    return redirect('listeProduits')

