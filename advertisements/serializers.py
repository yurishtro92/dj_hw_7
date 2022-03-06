from django.contrib.auth.models import User
from rest_framework import serializers, exceptions
from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        if len(Advertisement.objects.filter(creator_id=self.context["request"].user.id, status='OPEN')) > 10:
             raise exceptions.ValidationError("У пользователя более 10 открытых объявлений")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('status') == None:
            raise exceptions.ValidationError("Укажите статус объявления")
        if instance.status == 'CLOSED' and validated_data.get('status') == 'OPEN':
            if len(Advertisement.objects.filter(creator_id=self.context["request"].user.id, status='OPEN')) > 10:
                 raise exceptions.ValidationError("У пользователя более 10 открытых объявлений")
        if instance.creator == self.context["request"].user:
            return super().update(instance, validated_data)
        else:
            raise exceptions.PermissionDenied
            return


