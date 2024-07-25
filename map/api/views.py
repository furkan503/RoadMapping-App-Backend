from rest_framework import viewsets, status
from map.models import Datayol, Databolge
from map.api.serializers import DatayolSerializer, DatabolgeSerializer, UserSerializer
from map.api.pagination import Pagination
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from django.contrib.gis.geos import Polygon, LineString




class DatayolViewSet(viewsets.ModelViewSet):
    queryset = Datayol.objects.all().order_by('id')
    pagination_class = Pagination
    serializer_class = DatayolSerializer

    @action(detail=False, methods=['POST'], url_path='filter')
    def filter_data(self, request):
        try:
            polygon_coords = request.data.get('polygon', [])
            if not polygon_coords:
                return Response({'error': 'No polygon provided'}, status=400)
            geojson_features = []
            for i in polygon_coords:
                xxx = i['geometry']['coordinates'][0]
                if xxx[0] != xxx[-1]:
                    xxx.append(xxx[0])

                polygon = Polygon(xxx, srid=4326)

                # Filter objects within the provided polygon
                filtered_objects = Datayol.objects.filter(koordinat__within=polygon)

                # Manually construct GeoJSON response
            
                for obj in filtered_objects:
                    if obj.koordinat:  
                        feature = {
                            "type": "Feature",
                            "geometry": {
                                "type": "LineString",  
                                "coordinates": list(obj.koordinat.coords),  
                            },
                            "properties": {},
                        }
                        
                        # Collect all properties except 'koordinat'
                        for field in obj._meta.get_fields():
                            field_name = field.name
                            if field_name != 'koordinat':
                                feature["properties"][field_name] = getattr(obj, field_name)

                        geojson_features.append(feature)

                geojson_response = {
                    "type": "FeatureCollection",
                    "features": geojson_features,
                }

            return Response({'data': geojson_response, 'status': True})
        except Exception as e:
            return Response({'err_msg': str(e), 'status': False})

    @action(detail=False, methods=['POST', 'GET'], url_path='create')
    def create_line(self, request):
        try:
            coordinates = request.data.get('coordinates', [])
            yolhizlimiti = request.data.get('yolhizlimiti')
            yoltipi = request.data.get('yoltipi')
            yoladi = request.data.get('yoladi', None)
            yolbolge = request.data.get('yolbolge', None)
            yoltamadres = request.data.get('yoltamadres', None)

            if not coordinates:
                return Response({'error': 'Coordinates are required'}, status=400)

            line_string = LineString(coordinates, srid=4326)

            uzunluk = line_string.length

            centroid = line_string.centroid

            new_line = Datayol.objects.create(
                koordinat=line_string,
                yolhizlimiti=yolhizlimiti,
                yoltipi=yoltipi,
                yoladi=yoladi,
                yolbolge=yolbolge,
                merkezlat=line_string.centroid.y,
                merkezlong=line_string.centroid.x,
                yoltamadres=yoltamadres,
                uzunluk=uzunluk,

            )

            return Response({'status': 'success', 'data': DatayolSerializer(new_line).data}, status=201)

        except Exception as e:
            return Response({'error': str(e)}, status=400)
        

        


class DatabolgeViewSet(viewsets.ModelViewSet):
    queryset = Databolge.objects.all().order_by('id')
    serializer_class = DatabolgeSerializer
    pagination_class = Pagination


class LoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = Pagination
    @action(detail=False, methods=['POST', 'GET'],)
    def custom_login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            request.session['logged_in_message'] = 'User logged in successfully'

            return Response({
                'message': 'logged in',
                'access': access_token,
                'refresh': refresh_token,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'could not log in'}, status=status.HTTP_401_UNAUTHORIZED)
