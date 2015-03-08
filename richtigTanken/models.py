from django.db import models
from django.contrib.auth.models import User
# x und y-values in metern
# allgemiene Daten (ueber tankstellen-api zu holen)
class Tankstellen(models.Model):
	bezeichnung = models.CharField(max_length=256)
	position_x = models.DecimalField(max_digits = 8, decimal_places = 6)
	position_y = models.DecimalField(max_digits = 8, decimal_places = 6)

	def __unicode__(self):
		return self.bezeichnung

# preise werden auch gecrawled (ebenfalls tankstellen-api)
class BenzinPreis(models.Model):
	tankstelle = models.ForeignKey(Tankstellen)
	preis = models.DecimalField(max_digits = 5, decimal_places = 2)
	start_zeit = models.DateTimeField()

	def __unicode__(self):
		return(str(self.start_zeit))

	class Meta:
		ordering = ('start_zeit',)


class FahrtDaten(models.Model):
	nutzer = models.ForeignKey(User)
	strecken_laengekm = models.DecimalField(max_digits = 5, decimal_places = 1)
	spritverbrauch_in_l = models.DecimalField(max_digits = 4, decimal_places = 2)
	start_zeit = models.DateTimeField()
	end_zeit = models.DateTimeField()

	class Meta:
		ordering = ('end_zeit',)

# create user positions for mockup, updated jede minute
class UserPositions(models.Model):
	zeit = models.DateTimeField()
	benzin_delta_in_l = models.DecimalField(max_digits = 4, decimal_places = 2)
	position_x = models.DecimalField(max_digits = 8, decimal_places = 6)
	position_y = models.DecimalField(max_digits = 8, decimal_places = 6)

	class Meta:
		ordering = ('zeit',)

