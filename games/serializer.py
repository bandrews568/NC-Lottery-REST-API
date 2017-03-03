from rest_framework import serializers

from .models import (Pick3, Pick4, Cash5,
                     PowerBall, MegaMillions,
                     LuckyForLife)


class Pick3Serializer(serializers.ModelSerializer):
    class Meta:
        model = Pick3
        fields = ('drawing_time',
                  'drawing_date',
                  'drawing_numbers')


class Pick4Serializer(serializers.ModelSerializer):
    class Meta:
        model = Pick4
        fields = ('drawing_time',
                  'drawing_date',
                  'drawing_numbers')


class Cash5Serializer(serializers.ModelSerializer):
    class Meta:
        model = Cash5
        fields = ('drawing_date',
                  'drawing_numbers',
                  'jackpot')


class PowerBallSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerBall
        fields = ('drawing_date',
                  'drawing_numbers',
                  'powerball')


class MegaMillionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MegaMillions
        fields = ('drawing_date',
                  'drawing_numbers',
                  'megaball',
                  'multiplier')


class LuckyForLifeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LuckyForLife
        fields = ('drawing_date',
                  'drawing_numbers')
