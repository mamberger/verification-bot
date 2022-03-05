from rest_framework import serializers


class AccountSerializer(serializers.Serializer):
    status = serializers.BooleanField()
    accounts = serializers.JSONField()


class CardSerializer(serializers.Serializer):
    status = serializers.BooleanField()
    accounts = serializers.JSONField()