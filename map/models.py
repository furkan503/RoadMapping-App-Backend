from django.contrib.gis.db import models


class Databolge(models.Model):
    katmandegeri = models.IntegerField(blank=True, null=True)
    bolgeadi = models.CharField(max_length=250, blank=True, null=True)
    koordinat = models.PolygonField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'databolge'


class Datayol(models.Model):
    yoltipi = models.IntegerField(blank=True, null=True)
    yolhizlimiti = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    uzunluk = models.DecimalField(max_digits=15, decimal_places=5)
    koordinat = models.LineStringField(srid=4326,blank=True, null=True, spatial_index=True)
    yoladi = models.CharField(max_length=250, blank=True, null=True)
    yolbolge = models.CharField(max_length=250, blank=True, null=True)
    merkezlat = models.FloatField(blank=True, null=True)
    merkezlong = models.FloatField(blank=True, null=True)
    yoltamadres = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['koordinat']),
        ]
        managed = False
        db_table = 'datayol'
