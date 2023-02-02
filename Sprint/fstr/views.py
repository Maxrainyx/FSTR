from rest_framework import viewsets
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .serializers import PassAddedSerializer
from .models import Pass, User, PassImages


class PassViewset(viewsets.ModelViewSet):
    queryset = Pass.objects.all()
    serializer_class = PassAddedSerializer


@csrf_exempt
def submitData(request):
    if request.method == 'POST':
        json_params = json.loads(request.body)
        _pass = Pass.objects.create(
            date_added=json_params['date_added'],
            title=json_params['title'],
            bTitle=json_params['bTitle'],
            other_title=json_params['other_title'],
            connect=json_params['connect'],
            coord_id=User.objects.create(
                latitude=json_params['latitude'],
                longitude=json_params['longitude'],
                height=json_params['height'],
            ),
            spring=json_params['spring'],
            summer=json_params['summer'],
            autumn=json_params['autumn'],
            winter=json_params['winter'],
            user=User.objects.create(
                name=json_params['name'],
                surname=json_params['surname'],
                email=json_params['email'],
                mobile=json_params['mobile'],
            ),
            status=json_params['status'],
        )
        return HttpResponse(json.dumps({
            "title": _pass.title,
            "bTitle": _pass.bTitle,
            "other_title": _pass.other_title,
            "connect": _pass.connect,
            "coord_id": _pass.coord_id,
            "spring": _pass.spring,
            "summer": _pass.summer,
            "autumn": _pass.autumn,
            "pass_images": _pass.pass_images,
            "status": _pass.status,
            "user": _pass.user,
        }))
