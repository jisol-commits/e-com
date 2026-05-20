from django.core.management.base import BaseCommand

from shop.models import Category, Product


class Command(BaseCommand):
    help = "Seed the development database with luxury demo products."

    def handle(self, *args, **options):
        categories = {
            "timepieces": Category.objects.get_or_create(
                name="Timepieces",
                slug="timepieces",
                defaults={"description": "Precision watches with black ceramic and gold accents."},
            )[0],
            "leather": Category.objects.get_or_create(
                name="Leather Goods",
                slug="leather-goods",
                defaults={"description": "Structured carry pieces in rich black leather."},
            )[0],
            "fragrance": Category.objects.get_or_create(
                name="Fragrance",
                slug="fragrance",
                defaults={"description": "Warm, evening-ready scents for private occasions."},
            )[0],
            "jewelry": Category.objects.get_or_create(
                name="Jewelry",
                slug="jewelry",
                defaults={"description": "Gold-finished statement pieces with restrained lines."},
            )[0],
        }

        products = [
            {
                "category": categories["timepieces"],
                "name": "Aurum Nocturne Watch",
                "slug": "aurum-nocturne-watch",
                "tagline": "Swiss movement, black ceramic body, brushed gold bezel.",
                "description": "A slim evening timepiece with sapphire crystal, a textured matte dial, and luminous gold indices.",
                "price": "1240.00",
                "material": "Ceramic and gold vermeil",
                "stock": 8,
                "is_featured": True,
                "image_url": "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?auto=format&fit=crop&w=1200&q=80",
            },
            {
                "category": categories["leather"],
                "name": "Obsidian Leather Tote",
                "slug": "obsidian-leather-tote",
                "tagline": "Full-grain leather with polished brass detailing.",
                "description": "A structured tote made for travel days, private appointments, and the rhythm of a working wardrobe.",
                "price": "680.00",
                "material": "Italian leather",
                "stock": 12,
                "is_featured": True,
                "image_url": "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?auto=format&fit=crop&w=1200&q=80",
            },
            {
                "category": categories["fragrance"],
                "name": "Golden Hour Eau de Parfum",
                "slug": "golden-hour-eau-de-parfum",
                "tagline": "Amber, saffron, smoked vanilla, and midnight jasmine.",
                "description": "A warm extrait-style fragrance with a long drydown and a polished evening signature.",
                "price": "220.00",
                "material": "Extrait concentration",
                "stock": 30,
                "is_featured": True,
                "image_url": "https://images.unsplash.com/photo-1541643600914-78b084683601?auto=format&fit=crop&w=1200&q=80",
            },
            {
                "category": categories["jewelry"],
                "name": "Signet Noir Ring",
                "slug": "signet-noir-ring",
                "tagline": "Black onyx face set in a satin gold band.",
                "description": "A modern signet with architectural shoulders, made to be worn alone or stacked with quiet confidence.",
                "price": "390.00",
                "material": "Onyx and gold vermeil",
                "stock": 18,
                "is_featured": True,
                "image_url": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=1200&q=80",
            },
            {
                "category": categories["leather"],
                "name": "Midnight Card Case",
                "slug": "midnight-card-case",
                "tagline": "Compact black calfskin with a gold foil edge.",
                "description": "A slim everyday carry piece finished with hand-painted edges and a soft suede-lined center pocket.",
                "price": "145.00",
                "material": "Calfskin leather",
                "stock": 24,
                "is_featured": False,
                "image_url": "https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&w=1200&q=80",
            },
            {
                "category": categories["jewelry"],
                "name": "Imperial Cuff",
                "slug": "imperial-cuff",
                "tagline": "A clean gold cuff with a black enamel channel.",
                "description": "Minimal from a distance, richly detailed up close, with a mirror-polished interior and satin exterior.",
                "price": "520.00",
                "material": "Gold vermeil and enamel",
                "stock": 10,
                "is_featured": False,
                "image_url": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?auto=format&fit=crop&w=1200&q=80",
            },
        ]

        for product in products:
            Product.objects.update_or_create(slug=product["slug"], defaults=product)

        self.stdout.write(self.style.SUCCESS("Seeded Aurum Luxe demo catalog."))
