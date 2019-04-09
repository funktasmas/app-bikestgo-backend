# -*- coding: utf-8 -*-
import requests
import dateutil.parser
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from django.db.models import Sum
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from .models import Station, Data


def get_data_api():
    cache_key = 'data_bikesantiago'
    data = cache.get(cache_key)
    if data is None:
        r = requests.get(settings.API_BIKESTGO)
        data = []
        if r.status_code == 200:
            data = r.json()
            cache.set(cache_key, data, settings.API_CACHE)
    return data


def save_data_api():
    data = get_data_api()
    now = timezone.now()
    for station_api in data['network']['stations']:
        id_api = station_api['id']
        lat = station_api['latitude']
        lon = station_api['longitude']
        try:
            station_obj = Station.objects.get(id_api=id_api)
            if station_obj.latitude != lat:
                station_obj.latitude = lat
            if station_obj.longitude != lon:
                station_obj.longitude = lon
            if not station_obj.state or not station_obj.city:
                state, city = geolocation(lat, lon)
                station_obj.state = state
                station_obj.city = city
            station_obj.save()
        except Station.DoesNotExist:
            name = station_api['name'].split('-')
            state, city = geolocation(lat, lon)
            station_data = {
                'name': name[1].strip(),
                'nomenclature': name[0].strip(),
                'id_api': id_api,
                'latitude': lat,
                'longitude': lon,
                'state': state,
                'city': city,
            }
            station_obj = Station.objects.create(**station_data)

        data_station = {
            'free_bikes': station_api['free_bikes'],
            'empty_slots': station_api['empty_slots'],
            'date': now,
            'date_api': dateutil.parser.parse(station_api['timestamp']),
            'station': station_obj,
        }
        Data.objects.create(**data_station)


def get_stations():
    cache_key = 'stations'
    data = cache.get(cache_key)
    if data is None:
        all_stations = []
        total_free_bikes = 0
        total_empty_slots = 0

        for station in Station.objects.all():
            data_station = station.get_data_dict()
            all_stations.append(data_station)
            total_free_bikes = total_free_bikes + data_station['last']['free_bikes']
            total_empty_slots = total_empty_slots + data_station['last']['empty_slots']

        chart_bike_used = []
        for d in Data.objects.values('date').distinct():
            empty_slots = Data.objects.filter(date=d['date']).aggregate(Sum('empty_slots'))
            chart_bike_used.append({
                'x': d['date'].timestamp(),
                'y': empty_slots['empty_slots__sum']
            })
        data = {
            'stations': all_stations,
            'total_free_bikes': total_free_bikes,
            'total_empty_slots': total_empty_slots,
            'chart_bike_used': chart_bike_used
        }
    cache.set(cache_key, data, settings.API_CACHE)
    return data


def geolocation(lat, lon):
    geolocator = Nominatim(user_agent="geo_bikestgo")
    try:
        location = geolocator.reverse(f"{lat}, {lon}")
        state = location.raw['address']['state']
        city = location.raw['address']['city']
    except (GeocoderTimedOut, GeocoderServiceError, KeyError):
        state = None
        city = None
    return state, city
