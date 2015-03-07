from django.db import models
from django.contrib.auth.models import User
# x und y-values in metern
# allgemiene Daten (ueber tankstellen-api zu holen)
class Tankstellen(models.Model):
	bezeichnung = models.CharField(max_length=256)
	x_wert = models.IntegerField()
	y_wert = models.IntegerField()

# preise werden auch gecrawled (ebenfalls tankstellen-api)
class BenzinPreis(models.Model):
	tankstelle = models.ForeignKey(Tankstellen)
	preis = models.DecimalField(max_digits = 5, decimal_places = 2)
	start_zeit = models.DateTimeField()


class FahrtDaten(models.Model):
	nutzer = models.ForeignKey(User)
	strecken_laengekm = models.DecimalField(max_digits = 4, decimal_places = 1)
	spritverbrauch_in_l = models.DecimalField(max_digits = 4, decimal_places = 2)
	start_zeit = models.DateTimeField()
	end_zeit = models.DateTimeField()

# create user positions for mockup, updated jede minute
class UserPositions(models.Model):
	zeit = models.DateTimeField(auto_now = True)
	benzin_delta_in_l = models.DecimalField(max_digits = 4, decimal_places = 2)
	position_x = models.IntegerField()
	position_y = models.IntegerField()

