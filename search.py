from ecommerce_app.models import Inventory 

def search_products(query, category=None, filters=None):
    
    results = Inventory.objects.all() 

    if query:
        results = results.filter(name__icontains=query)

    if category:
        results = results.filter(category__iexact=category)

    if filters:
        for key, value in filters.items():
            results = results.filter(**{key: value})

    results = [
        {"name": product.name, "price": product.price, "seller": product.seller, "category": product.category} 
        for product in results
    ]

    return results


