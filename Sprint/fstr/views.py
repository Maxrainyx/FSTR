from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Pass, User, Level, Coordinates, Images
from .serializers import (
    PassSerializer, ImagesSerializer, UserSerializer, CoordinatesSerializer, LevelSerializer
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view


def reverse_to_submit(request):
    """ Redirects to submitData """
    return redirect('submitData')


class PassAPIView(viewsets.ViewSet):
    """ API endpoint that allows users to look up records or edited them. """

    @staticmethod
    def serializer_error_response(errors, param='id'):
        """ Response method for serializer errors. Method is static method."""
        message = ''
        for k, v in errors.items():
            message += f'{k}: {str(*v)}'
        if param == 'state':
            return Response({'message': message, 'state': 0}, status=400)
        else:
            return Response({'message': message, 'id': None}, status=400)

    def create_dependence(self, serializer):
        """ Create dependence method. """
        if serializer.is_valid():
            return serializer.save()
        else:
            return self.serializer_error_response(serializer.errors)

    @swagger_auto_schema(methods=['post'], request_body=PassSerializer)
    @api_view(['POST'])
    def post(self, request):
        """ Swagger auto schema for post method. """
        try:
            data = request.data
            if not data:
                return Response({'message': 'Empty request', 'id': None}, status=400)

            try:
                user = User.objects.get(email=data['user']['email'])
                user_serializer = UserSerializer(user, data=data['user'])
            except:
                user_serializer = UserSerializer(data=data['user'])

            try:
                images = data['images']
                data.pop('images')
            except:
                images = []

            serializer = PassSerializer(data=data)
            if serializer.is_valid():
                try:
                    data.pop('user')
                    pass_new = Pass.objects.create(
                        user=self.create_dependence(user_serializer),
                        coords=self.create_dependence(CoordinatesSerializer(data=data.pop('coordinates'))),
                        levels=self.create_dependence(LevelSerializer(data=data.pop('level'))),
                        **data)
                except Exception as e:
                    return Response({'message': str(e), 'id': None}, status=400)
            else:
                return self.serializer_error_response(serializer.errors)

            for image in images:
                image['pass'] = pass_new.id
                self.create_dependence(ImagesSerializer(data=image))

            return Response({'message': 'Success', 'id': pass_new.id}, status=200)

        except Exception as e:
            return Response({'message': str(e), 'id': None}, status=500)

    @swagger_auto_schema(metods=['get'], manual_parameters=[
        openapi.Parameter('user_email', openapi.IN_QUERY, description="user e-mail", type=openapi.TYPE_STRING)])
    def get_records_by_user(self, request, **kwargs):
        """ Get records for the user. """
        try:
            user = User.objects.get(email=request.GET['user_email'])
            passages = Pass.objects.filter(user=user)
            data = PassSerializer(passages, many=True).data
            return Response(data, status=200)
        except:
            return Response({'message': 'No records found'}, status=200)

    @swagger_auto_schema(metods=['get'], request_body=PassSerializer)
    def get_one(self, request, **kwargs):
        """ Get one record. """
        try:
            pass_one = Pass.objects.get(pk=kwargs['pk'])
            data = PassSerializer(pass_one).data
            return Response(data, status=200)
        except:
            return Response({'message': "There's no such record", 'id': None}, status=400)

    @swagger_auto_schema(metods=['patch'], request_body=PassSerializer)
    def edit_one(self, request, **kwargs):
        """ Edit one record. """
        try:
            pass_one = Pass.objects.get(pk=kwargs['pk'])
            if pass_one.status == 'new':
                data = request.data
                data.pop('user')
                Images.objects.filter(pereval_id=pass_one.id).delete()
                images = data.pop('images')
                serializers = []
                serializers.append(CoordinatesSerializer(Coordinates.objects.get(id=pass_one.coordsinates_id),
                                                         data=data.pop('coordinates')))
                serializers.append(LevelSerializer(Level.objects.get(id=pass_one.levels_id), data=data.pop('level')))
                serializers.append((PassSerializer(pass_one, data=data)))
                for image in images:
                    image['pass'] = pass_one.id
                    serializers.append(ImagesSerializer(data=image))
                for serializer in serializers:
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return self.serializer_error_response(serializer.errors, 'state')
                return Response({'message': 'Success', 'state': 1}, status=200)
            else:
                return Response({'message': "It's not a new status of the record", 'state': 0}, status=400)
        except:
            return Response({'message': "There's no such record", 'state': 0}, status=400)
