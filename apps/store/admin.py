# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Station, Data


class DataInline(admin.StackedInline):
    model = Data
    extra = 0


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('id', 'nomenclature', 'name', 'state', 'city')
    search_fields = ['name']
    list_filter = ['state', 'city']
    list_per_page = 100
    inlines = [DataInline]
