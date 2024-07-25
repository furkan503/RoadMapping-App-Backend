from django.contrib.gis import admin
from .models import Datayol, Databolge
from leaflet.admin import LeafletGeoAdmin


@admin.register(Datayol)
class DatayolAdmin(LeafletGeoAdmin):
    list_display = ('yoladi', 'yolbolge', 'koordinat')

@admin.register(Databolge)
class DatabolgeAdmin(LeafletGeoAdmin):
    list_display = ('bolgeadi', 'koordinat')