from django.contrib import admin

# Register your models here.
from .models import Product, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug", "active")
    search_fields = ("title", "slug")
    ordering = (
        "-id",
        "-title",
    )
    list_per_page = 10
    list_display_links = ("id", "title")


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "price",
        "category__id",
        "active",
    )
    list_filter = ("title", "category__id", "price", "active")
    search_fields = ("title", "category__id")
    ordering = (
        "-price",
        "-title",
        "-id",
    )
    list_per_page = 10


admin.site.register(Product, ProductAdmin)
