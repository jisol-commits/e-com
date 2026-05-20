from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def _fallback_products():
    return [
        {
            "name": "Neo RTX 4080 Dragon OC",
            "slug": "neo-rtx-4080-dragon-oc",
            "tagline": "16GB GDDR6X graphics card with ray tracing power and elite cooling.",
            "price": 1199,
            "material": "16GB GDDR6X / PCIe 4.0",
            "display_image": "https://images.unsplash.com/photo-1591488320449-011701bb6704?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Neo Fury DDR5 RGB RAM",
            "slug": "neo-fury-ddr5-rgb-ram",
            "tagline": "32GB low-latency DDR5 kit tuned for high-FPS gaming builds.",
            "price": 169,
            "material": "32GB / DDR5-6000 / CL30",
            "display_image": "https://images.unsplash.com/photo-1562976540-1502c2145186?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Neo Ryzen 9 Apex CPU",
            "slug": "neo-ryzen-9-apex-cpu",
            "tagline": "16-core desktop processor for gaming, streaming, and rendering.",
            "price": 549,
            "material": "16 Cores / 32 Threads",
            "display_image": "https://images.unsplash.com/photo-1555617981-dac3880eac6e?auto=format&fit=crop&w=1200&q=80",
        },
    ]


def home(request):
    featured = list(Product.objects.select_related("category").filter(is_featured=True)[:9])
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
