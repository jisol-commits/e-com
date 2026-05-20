from django.contrib import admin

from .models import Category, OrderLead, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "is_featured")
    list_filter = ("category", "is_featured")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "tagline", "description")


@admin.register(OrderLead)
class OrderLeadAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "product", "created_at")
    search_fields = ("full_name", "email")
