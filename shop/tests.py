from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class StorefrontSmokeTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Timepieces", slug="timepieces")
        self.product = Product.objects.create(
            category=self.category,
            name="Aurum Nocturne Watch",
            slug="aurum-nocturne-watch",
            tagline="Swiss movement and gold bezel.",
            description="A refined black and gold watch.",
            price="1240.00",
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
