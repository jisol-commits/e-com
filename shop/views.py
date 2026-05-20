from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def _fallback_products():
    return [
        {
            "name": "Aurum Nocturne Watch",
            "slug": "aurum-nocturne-watch",
            "tagline": "Swiss movement, black ceramic body, brushed gold bezel.",
            "price": 1240,
            "material": "Ceramic and gold vermeil",
            "display_image": "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Obsidian Leather Tote",
            "slug": "obsidian-leather-tote",
            "tagline": "Full-grain leather with polished brass detailing.",
            "price": 680,
            "material": "Italian leather",
            "display_image": "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Golden Hour Eau de Parfum",
            "slug": "golden-hour-eau-de-parfum",
            "tagline": "Amber, saffron, smoked vanilla, and midnight jasmine.",
            "price": 220,
            "material": "Extrait concentration",
            "display_image": "https://images.unsplash.com/photo-1541643600914-78b084683601?auto=format&fit=crop&w=1200&q=80",
        },
    ]


def home(request):
    featured = list(Product.objects.select_related("category").filter(is_featured=True)[:6])
    if not featured:
        featured = _fallback_products()
    return render(
        request,
        "shop/home.html",
        {
            "featured_products": featured,
            "categories": Category.objects.all()[:6],
        },
    )


def collection(request):
    active_category = request.GET.get("category")
    products = Product.objects.select_related("category").all()
    if active_category:
        products = products.filter(category__slug=active_category)

    products = list(products)
    if not products and not active_category:
        products = _fallback_products()

    return render(
        request,
        "shop/collection.html",
        {
            "products": products,
            "categories": Category.objects.all(),
            "active_category": active_category,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:3]
    return render(
        request,
        "shop/product_detail.html",
        {"product": product, "related_products": related_products},
    )
