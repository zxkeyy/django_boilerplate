from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Profile) 
class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user']