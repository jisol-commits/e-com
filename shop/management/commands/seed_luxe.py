from django.core.management.base import BaseCommand

from shop.models import Category, Product


class Command(BaseCommand):
    help = "Seed the development database with premium PC component demo products."

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        categories = {
            "graphics_cards": Category.objects.get_or_create(
                name="Graphics Cards",
                slug="graphics-cards",
                defaults={"description": "High-performance GPUs for gaming, rendering, and AI workloads."},
            )[0],
            "memory": Category.objects.get_or_create(
                name="RAM",
                slug="ram",
                defaults={"description": "Fast DDR5 memory kits for gaming and creator builds."},
            )[0],
            "processors": Category.objects.get_or_create(
                name="Processors",
                slug="processors",
                defaults={"description": "Desktop CPUs for speed, efficiency, and multitasking."},
            )[0],
            "motherboards": Category.objects.get_or_create(
                name="Motherboards",
                slug="motherboards",
                defaults={"description": "Feature-rich boards with modern chipsets and expansion."},
            )[0],
            "storage": Category.objects.get_or_create(
                name="Storage",
                slug="storage",
                defaults={"description": "NVMe SSDs and drives for fast boot and load times."},
            )[0],
            "power_cooling": Category.objects.get_or_create(
                name="Power & Cooling",
                slug="power-cooling",
                defaults={"description": "Reliable PSUs, liquid coolers, and airflow essentials."},
            )[0],
        }

        products = [
            {
                "category": categories["graphics_cards"],
                "name": "Neo RTX 4080 Dragon OC",
                "slug": "neo-rtx-4080-dragon-oc",
                "tagline": "16GB GDDR6X graphics card with ray tracing power and elite cooling.",
                "description": "A premium triple-fan GPU for 4K gaming, rendering, and streaming, finished with a reinforced backplate and black-and-gold showcase styling.",
                "price": "1199.00",
                "material": "16GB GDDR6X / PCIe 4.0",
                "stock": 8,
                "is_featured": True,
                "image_url": "https://images.unsplash.com/photo-1591488320449-011701bb6704?auto=format&fit=crop&w=1200&q=80",
            },
            {
                "category": categories["memory"],
                "name": "Neo Fury DDR5 RGB RAM",
                "slug": "neo-fury-ddr5-rgb-ram",
                "tagline": "32GB low-latency DDR5 kit tuned for high-FPS gaming builds.",
                "description": "A 2x16GB performance memory kit with premium heat spreaders, stable XMP profiles, and warm gold lighting accents.",
                "price": "169.00",
                "material": "32GB / DDR5-6000 / CL30",
                "stock": 22,
                "is_featured": True,
                "image_url": "https://images.unsplash.com/photo-1562976540-1502c2145186?auto=format&fit=crop&w=1200&q=80",
            },
            {
                "category": categories["processors"],
                "name": "Neo Ryzen 9 Apex CPU",
                "slug": "neo-ryzen-9-apex-cpu",
                "tagline": "16-core desktop processor for gaming, streaming, and rendering.",
                "description": "A high-end CPU selected for fast boost clocks, strong multicore output, and smooth performance in demanding PC builds.",
                "price": "549.00",
                "material": "16 Cores / 32 Threads",
                "stock": 14,
                "is_featured": True,
                "image_url": "https://images.unsplash.com/photo-1555617981-dac3880eac6e?auto=format&fit=crop&w=1200&q=80",
            },
            {
                "category": categories["motherboards"],
                "name": "Neo X670E Carbon Board",
                "slug": "neo-x670e-carbon-board",
                "tagline": "ATX motherboard with PCIe 5.0, Wi-Fi 7, and premium VRM cooling.",
                "description": "A feature-rich board for enthusiast builds with reinforced slots, clean cable routing, and a polished black PCB.",
                "price": "429.00",
                "material": "ATX / PCIe 5.0 / Wi-Fi 7",
                "stock": 18,
                "is_featured": True,
                "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
            },
            {
                "category": categories["storage"],
                "name": "NeoSpeed Gen4 NVMe SSD",
                "slug": "neospeed-gen4-nvme-ssd",
                "tagline": "2TB NVMe drive for ultra-fast boot, game, and project loading.",
                "description": "A high-speed M.2 SSD with a slim heat spreader, strong sustained writes, and dependable performance for modern desktops.",
                "price": "189.00",
                "material": "2TB / PCIe Gen4 / M.2",
                "stock": 24,
                "is_featured": False,
                "image_url": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?auto=format&fit=crop&w=1200&q=80",
            },
            {
                "category": categories["power_cooling"],
                "name": "NeoVolt 850W Gold PSU",
                "slug": "neovolt-850w-gold-psu",
                "tagline": "Modular 850W power supply with 80 Plus Gold efficiency.",
                "description": "A quiet, fully modular PSU designed for powerful GPUs, tidy cable management, and stable long-term performance.",
                "price": "159.00",
                "material": "850W / Fully Modular",
                "stock": 10,
                "is_featured": False,
                "image_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=1200&q=80",
            },
        ]

        for product in products:
            Product.objects.update_or_create(slug=product["slug"], defaults=product)

        self.stdout.write(self.style.SUCCESS("Seeded Neo China PC components catalog."))
