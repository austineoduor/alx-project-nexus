from rest_framework import serializers

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(allow_blank=True)
    overview = serializers.CharField(allow_blank=True)
    popularity = serializers.FloatField(required=False)
    vote_average = serializers.FloatField(required=False)
    release_date = serializers.CharField(required=False)
    poster_path = serializers.CharField(required=False, allow_null=True)