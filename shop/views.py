import json
import os
from urllib import error, request

from django.db.models import Q
from django.http import JsonResponse
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
            "name": "Neo Eclipse 4070",
            "slug": "neo-eclipse-4070",
            "tagline": "Premium 1440p gaming PC with clean glass styling and balanced performance.",
            "price": 1899,
            "material": "RTX 4070 / Ryzen 7 / 32GB memory",
            "display_image": "https://images.unsplash.com/photo-1593640408182-31c70c8268f5?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Neo Stealth Gamer S5",
            "slug": "neo-stealth-gamer-s5",
            "tagline": "Compact, performance-focused gaming PC with sleek dark styling.",
            "price": 1699,
            "material": "RTX 4060 Ti / Ryzen 5 / 16GB memory",
            "display_image": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Neo Rift Elite",
            "slug": "neo-rift-elite",
            "tagline": "High-end desktop for streaming, gaming, and intense multitasking.",
            "price": 3599,
            "material": "RTX 4080 Ti / Core i9 / 64GB memory",
            "display_image": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=1200&q=80",
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


def _store_context(limit=12):
    products = Product.objects.select_related("category").filter(stock__gt=0).order_by("-is_featured", "name")[:limit]
    return "\n".join(
        f"- {product.name} ({product.category.name}): {product.tagline} ${product.price}"
        for product in products
    )


def _ask_openai(message):
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None

    payload = {
        "model": os.environ.get("OPENAI_MODEL", "gpt-5"),
        "instructions": (
            "You are Neo China's concise e-commerce shopping assistant. "
            "Help customers choose PC components, prebuilt PCs, cabinets, keyboards, mice, audio gear, shipping, and returns. "
            "Never invent products or policies. If asked about products, use this current store inventory context:\n"
            f"{_store_context()}"
        ),
        "input": message,
    }
    api_request = request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(api_request, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (error.HTTPError, error.URLError, TimeoutError, json.JSONDecodeError):
        return None

    output_text = data.get("output_text")
    if output_text:
        return output_text.strip()

    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text" and content.get("text"):
                return content["text"].strip()
    return None


def chatbot_response(request):
    message = request.GET.get("message", "").strip()
    if not message:
        return JsonResponse(
            {"reply": "Ask me about products, shipping, returns, prebuilt PCs, cabinets, or finding the best components."}
        )

    text = message.lower()
    products = _find_products_for_query(message)
    ai_reply = _ask_openai(message)
    if ai_reply:
        return JsonResponse({"reply": ai_reply})

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
                        "For a gaming build, I recommend a powerful GPU, a fast CPU, a strong cabinet, and reliable cooling. "
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
                    "Use the category filters there to find GPUs, CPUs, cabinets, prebuilt PCs, motherboards, and more."
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
        f'<li><a href="{product.get_absolute_url()}">{product.name}</a> - {product.tagline}</li>'
        for product in products
    )
    return (
        f"<p>Here are some store recommendations you can browse directly:</p>"
        f"<ul>{items}</ul>"
    )
