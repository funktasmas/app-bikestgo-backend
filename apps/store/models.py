# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.db import models
from django.conf import settings


class Station(models.Model):
    id = models.AutoField('id', primary_key=True)
    name = models.CharField(max_length=200)
    nomenclature = models.CharField(max_length=200)
    id_api = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    state = models.CharField(max_length=200, blank=False, null=True)
    city = models.CharField(max_length=200, blank=False, null=True)

    def delete_cache(self):
        cache.delete('stations')

    def __str__(self):
        return f'{self.id}: {self.name}'

    def delete(self, **kwargs):
        self.delete_cache()
        super(Station, self).delete()

    def save(self, **kwargs):
        self.delete_cache()
        super(Station, self).save()

    def get_data(self):
        cache_key = f'data_station_{self.id}'
        data = cache.get(cache_key)
        if data is None:
            data = Data.objects.filter(station=self)
            cache.set(cache_key, data, settings.API_CACHE)
        return data

    def get_last_data(self):
        try:
            last = self.get_data().latest('date')
            return last.get_data_dict()
        except Data.DoesNotExist:
            return {}

    def get_data_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'id_api': self.id_api,
            'city': self.city,
            'last': self.get_last_data(),
        }

    class Meta:
        verbose_name = ('station')
        verbose_name_plural = ('stations')
        unique_together = ['id_api']


class Data(models.Model):
    free_bikes = models.PositiveIntegerField(default=0)  # bicis disponibles
    empty_slots = models.PositiveIntegerField(default=0)  # vacantes libres
    date_api = models.DateTimeField()
    date = models.DateTimeField()
    # fk
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='station')

    def delete_cache(self):
        cache.delete(f'data_station_{self.station.id}')

    def __str__(self):
        return f'{self.id}'

    def delete(self, **kwargs):
        self.delete_cache()
        super(Data, self).delete()

    def save(self, **kwargs):
        self.delete_cache()
        super(Data, self).save()

    class Meta:
        verbose_name = ('data')
        verbose_name_plural = ('data')
        unique_together = ['date', 'station']

    def get_data_dict(self):
        return {
            'free_bikes': self.free_bikes,
            'empty_slots': self.empty_slots,
            'date_api': self.date_api.timestamp(),
        }
