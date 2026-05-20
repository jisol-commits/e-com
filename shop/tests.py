from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class StorefrontSmokeTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Graphics Cards", slug="graphics-cards")
        self.product = Product.objects.create(
            category=self.category,
            name="Aurum RTX 4080 Ultra GPU",
            slug="aurum-rtx-4080-ultra-gpu",
            tagline="16GB GDDR6X graphics card built for 4K gaming.",
            description="A premium black and gold graphics card.",
            price="1199.00",
            stock=4,
            is_featured=True,
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse("shop:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aurum Luxe")

    def test_collection_page_loads(self):
        response = self.client.get(reverse("shop:collection"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_detail_loads(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.tagline)
