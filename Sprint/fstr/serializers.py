from .models import Pass
from rest_framework import serializers


class PassAddedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pass
        fields = ['id',
                  'name',
                  'bTitle',
                  'title',
                  'other_title',
                  'connect',
                  'coord_id',
                  'spring',
                  'summer',
                  'autumn',
                  'winter',
                  'pass_images',
                  'status',
                  ]

