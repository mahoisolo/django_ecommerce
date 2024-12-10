from django.contrib import admin
from . import models
from django.utils.html import format_html
from django.contrib.contenttypes.admin import GenericTabularInline
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':['title']}
    list_display = ('title', 'price','inventory_status','Collections_title')
    list_editable=['price']
    list_filter=['Collections','last_update']

    def Collections_title(self,product):
        return product.Collections.title
    def Product_count(self,Collections):
        return Collections.Product_count

    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory<100:
            return 'low'
        return 'ok'
    # list_editable = ('price',)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'membership')
    list_editable=['membership']
    list_select_related=['user']
    ordering=['user__first_name']
    search_fields=['first_name__istartswith','last_name__istartswith']
    # list_per_page=10
admin.site.register(models.Collections)
admin.site.register(models.Product,ProductAdmin)
admin.site.register(models.Customer,CustomerAdmin)
