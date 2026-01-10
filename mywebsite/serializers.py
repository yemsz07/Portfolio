from rest_framework import serializers
from .models import myweb

class MyWebSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = myweb
        fields = [
            'id',
            'user',
            'description',
            'image',
            'pub_date',
            'updated_at',
        ]
