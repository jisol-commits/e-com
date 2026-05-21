from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

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


def _find_products_for_query(query, limit=3):
    return Product.objects.filter(
        Q(name__icontains=query)
        | Q(tagline__icontains=query)
        | Q(description__icontains=query)
        | Q(category__name__icontains=query)
        | Q(category__slug__icontains=query)
    ).distinct()[:limit]


def _top_products(limit=3):
    return Product.objects.filter(stock__gt=0).order_by("-is_featured", "name")[:limit]


def chatbot_response(request):
    message = request.GET.get("message", "").strip()
    if not message:
        return JsonResponse(
            {"reply": "Ask me about products, shipping, returns, or finding the best components."}
        )

    text = message.lower()
    products = _find_products_for_query(message)

    if "shipping" in text or "delivery" in text or "ship" in text:
        return JsonResponse(
            {
                "reply": (
                    "Most orders ship within 1-2 business days, and we typically deliver "
                    "quickly across the US. Ask about express options or your target delivery date "
                    "if you need an exact estimate."
                )
            }
        )

    if "return" in text or "refund" in text or "exchange" in text:
        return JsonResponse(
            {
                "reply": (
                    "We want you to love your purchase. Returns are accepted for unused items "
                    "within 30 days of delivery, and exchanges are available when the item is in stock."
                )
            }
        )

    if any(term in text for term in ["gpu", "graphics", "video card", "graphics card"]):
        category_products = products if products.exists() else _find_products_for_query("graphics")
        if not category_products.exists():
            fallback_products = _top_products()
            return JsonResponse(
                {
                    "reply": (
                        "We don't have GPU products matched exactly right now, but here are some popular store products you can browse."
                    ),
                    "reply_html": _build_product_recommendations(fallback_products),
                }
            )
        return JsonResponse(
            {
                "reply": (
                    "Our top GPUs are designed for high-performance gaming and creative work. "
                    "Here are the best matches available now."
                ),
                "reply_html": _build_product_recommendations(category_products),
            }
        )

    if any(term in text for term in ["ram", "memory", "ddr5", "ddr4"]):
        category_products = products if products.exists() else _find_products_for_query("ram")
        if not category_products.exists():
            fallback_products = _top_products()
            return JsonResponse(
                {
                    "reply": (
                        "I don't have RAM products in the store right now, but here are some popular items you might like."
                    ),
                    "reply_html": _build_product_recommendations(fallback_products),
                }
            )
        return JsonResponse(
            {
                "reply": (
                    "We carry high-speed RAM kits for modern gaming rigs and workstation builds. "
                    "These are great choices right now."
                ),
                "reply_html": _build_product_recommendations(category_products),
            }
        )

    if any(term in text for term in ["cpu", "processor", "ryzen", "intel"]):
        category_products = products if products.exists() else _find_products_for_query("processor")
        if not category_products.exists():
            fallback_products = _top_products()
            return JsonResponse(
                {
                    "reply": (
                        "I don't have CPU matches for that query at the moment, but here are some popular store products you can explore."
                    ),
                    "reply_html": _build_product_recommendations(fallback_products),
                }
            )
        return JsonResponse(
            {
                "reply": (
                    "Our CPUs fit gaming, streaming, and productivity builds. "
                    "Here are some top CPU options from the store."
                ),
                "reply_html": _build_product_recommendations(category_products),
            }
        )

    if any(term in text for term in ["motherboard", "mobo", "socket"]):
        category_products = products if products.exists() else _find_products_for_query("motherboard")
        if not category_products.exists():
            fallback_products = _top_products()
            return JsonResponse(
                {
                    "reply": (
                        "I don't have motherboard matches for that query right now, but here are some store favorites."
                    ),
                    "reply_html": _build_product_recommendations(fallback_products),
                }
            )
        return JsonResponse(
            {
                "reply": (
                    "Motherboards are chosen based on CPU compatibility, expansion, and features. "
                    "These boards are a good fit for modern builds."
                ),
                "reply_html": _build_product_recommendations(category_products),
            }
        )

    if any(term in text for term in ["ssd", "nvme", "storage", "hard drive"]):
        category_products = products if products.exists() else _find_products_for_query("storage")
        if not category_products.exists():
            fallback_products = _top_products()
            return JsonResponse(
                {
                    "reply": (
                        "I don't have storage matches for that query at the moment, but here are some top products from the store."
                    ),
                    "reply_html": _build_product_recommendations(fallback_products),
                }
            )
        return JsonResponse(
            {
                "reply": (
                    "We offer fast SSDs and NVMe drives for gaming and content creation. "
                    "These storage picks are available now."
                ),
                "reply_html": _build_product_recommendations(category_products),
            }
        )

    if any(term in text for term in ["psu", "power supply", "watt", "watts"]):
        category_products = products if products.exists() else _find_products_for_query("power")
        if not category_products.exists():
            fallback_products = _top_products()
            return JsonResponse(
                {
                    "reply": (
                        "I don't have power supply matches for that query right now, but here are some popular items from the store."
                    ),
                    "reply_html": _build_product_recommendations(fallback_products),
                }
            )
        return JsonResponse(
            {
                "reply": (
                    "A quality PSU is important for stability. Choose one with enough wattage "
                    "for your GPU, CPU, and future upgrades. These options are in stock."
                ),
                "reply_html": _build_product_recommendations(category_products),
            }
        )

    if any(term in text for term in ["build", "recommend", "best", "suggest"]):
        top_products = Product.objects.filter(stock__gt=0).order_by("-is_featured", "name")[:3]
        if "gaming" in text:
            return JsonResponse(
                {
                    "reply": (
                        "For a gaming build, I recommend a powerful GPU, a fast CPU, and plenty of RAM. "
                        "Here are some top options from the store."
                    ),
                    "reply_html": _build_product_recommendations(top_products),
                }
            )
        if "stream" in text or "content" in text or "video" in text:
            return JsonResponse(
                {
                    "reply": (
                        "For streaming or content creation, prioritize a strong CPU, fast storage, and a reliable GPU. "
                        "These picks are a great starting point."
                    ),
                    "reply_html": _build_product_recommendations(top_products),
                }
            )
        return JsonResponse(
            {
                "reply": (
                    "Tell me whether you're building for gaming, streaming, productivity, or general use, "
                    "and I can suggest the right parts."
                )
            }
        )

    if "price" in text or "cost" in text or "how much" in text:
        return JsonResponse(
            {
                "reply": (
                    "Prices vary by component, but I can guide you to premium or budget choices. "
                    "Ask about a specific part type and I can point you to the right products."
                )
            }
        )

    if "deal" in text or "sale" in text or "discount" in text:
        return JsonResponse(
            {
                "reply": (
                    "We frequently feature competitive pricing on performance components. "
                    "Check the collection page for the latest offers, or ask me about specific parts."
                )
            }
        )

    if "collection" in text or "browse" in text or "products" in text:
        return JsonResponse(
            {
                "reply": (
                    "The collection page shows the full selection of products. "
                    "Use the category filters there to find GPUs, CPUs, RAM, motherboards, and more."
                )
            }
        )

    if "support" in text or "help" in text or "question" in text:
        return JsonResponse(
            {
                "reply": (
                    "I can help with product selection, shipping, returns, and order guidance. "
                    "Ask me anything about choosing components or navigating this store."
                )
            }
        )

    if products.exists():
        return JsonResponse(
            {
                "reply": (
                    "I found these products based on your query. "
                    "Click a link to learn more."
                ),
                "reply_html": _build_product_recommendations(products),
            }
        )

    top_products = Product.objects.filter(stock__gt=0).order_by("-is_featured", "name")[:3]
    return JsonResponse(
        {
            "reply": (
                "I can answer questions about store items, shipping, returns, and custom PC builds. "
                "Here are a few popular products from the store if you want to browse."
            ),
            "reply_html": _build_product_recommendations(top_products),
        }
    )


def _build_product_recommendations(products):
    if not products:
        return ""

    items = "".join(
        f'<li><a href="{product.get_absolute_url()}">{product.name}</a> — {product.tagline}</li>'
        for product in products
    )
    return (
        f"<p>Here are some store recommendations you can browse directly:</p>"
        f"<ul>{items}</ul>"
    )


def _find_products_for_query(query, limit=3):
    return Product.objects.filter(
        Q(name__icontains=query)
        | Q(tagline__icontains=query)
        | Q(category__name__icontains=query)
    ).distinct()[:limit]
