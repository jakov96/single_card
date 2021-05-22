from django.contrib import admin
from catalog.models import Category, Service, Achievement, Card


class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class ServiceModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Service, ServiceModelAdmin)
admin.site.register(Card)
admin.site.register(Achievement)
