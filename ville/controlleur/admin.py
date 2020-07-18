from django.contrib import admin
from .models import Objet


# Register your models here.
@admin.register(Objet)
class objetAdmin(admin.ModelAdmin):
    pass
