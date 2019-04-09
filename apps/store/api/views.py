# -*- coding: utf-8 -*-
from rest_framework import status as status_rest
from rest_framework.views import APIView
from rest_framework.response import Response
from ..process import get_stations


class stations(APIView):
    def get(self, request):
        status = status_rest.HTTP_200_OK
        return Response(get_stations(), status=status)
