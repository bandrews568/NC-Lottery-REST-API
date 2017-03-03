from django.db import models

GAME_TIME = (
    ('D', 'Day'),
    ('E', 'Evening')
)


class Pick3(models.Model):
    drawing_time = models.CharField(max_length=1, choices=GAME_TIME)
    drawing_date = models.DateField()
    drawing_numbers = models.CommaSeparatedIntegerField(max_length=100)


class Pick4(models.Model):
    drawing_time = models.CharField(max_length=1, choices=GAME_TIME)
    drawing_date = models.DateField()
    drawing_numbers = models.CommaSeparatedIntegerField(max_length=100)


class Cash5(models.Model):
    drawing_date = models.DateField()
    drawing_numbers = models.CommaSeparatedIntegerField(max_length=100)
    jackpot = models.IntegerField()


class PowerBall(models.Model):
    drawing_date = models.DateField()
    drawing_numbers = models.CommaSeparatedIntegerField(max_length=100)
    powerball = models.IntegerField()


class MegaMillions(models.Model):
    drawing_date = models.DateField()
    drawing_numbers = models.CommaSeparatedIntegerField(max_length=100)
    megaball = models.IntegerField()
    multiplier = models.IntegerField(null=True)


class LuckyForLife(models.Model):
    drawing_date = models.DateField()
    drawing_numbers = models.CommaSeparatedIntegerField(max_length=100)
