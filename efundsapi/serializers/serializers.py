from rest_framework import serializers


class EfundsSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    description = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)
    deleted_at = serializers.DateTimeField(required=False)
    deleted = serializers.BooleanField(required=False)


class DemoSerializer(EfundsSerializer):
    uuid = serializers.CharField(read_only=True)
