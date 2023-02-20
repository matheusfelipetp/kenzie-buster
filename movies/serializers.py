from rest_framework import serializers

from .models import Movie, MovieOrder, Rating


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, allow_null=True, default=None)
    rating = serializers.ChoiceField(choices=Rating.choices, default=Rating.G)
    synopsis = serializers.CharField(allow_null=True, default=None)
    added_by = serializers.SerializerMethodField(read_only=True)

    def get_added_by(self, data):
        return data.user.email

    def create(self, validated_data: dict):
        movie = Movie.objects.create(**validated_data)
        return movie


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    buyed_by = buyed_by = serializers.SerializerMethodField(read_only=True)
    buyed_at = serializers.DateTimeField(read_only=True)

    def get_title(self, obj):
        return obj.order_movie.title

    def get_buyed_by(self, obj):
        return obj.order_user.email

    def create(self, validated_data):
        return MovieOrder.objects.create(**validated_data)
