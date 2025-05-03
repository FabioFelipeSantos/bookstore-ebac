from django.contrib import admin

# Register your models here.
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user__username",
        "product__title",
    )
    list_filter = ("product__active",)
    search_fields = ("user__username", "product__name")
    ordering = ("-id", "product__title")
    list_per_page = 10


admin.site.register(Order, OrderAdmin)
