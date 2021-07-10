from django.contrib import admin
from .models import Account

class PizzaAdmin (admin.ModelAdmin):
    list_display=('userName','password')
    search_fields = ['userName']

# Register your models here.

admin.site.register(Account, PizzaAdmin)
