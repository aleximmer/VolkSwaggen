from models import BenzinPreis, Tankstellen
import random

def addTankstellendaten(ident, offset):
	print(ident)
	print(offset)
	if ident < 2:
		return None
	station = Tankstellen.objects.all().get(pk=ident)
	finished_station = Tankstellen.objects.all().get(pk=1)
	preise = BenzinPreis.objects.all().filter(tankstelle=finished_station)
	for elem in preise:
		BenzinPreis.objects.create(tankstelle=station, preis=(float(elem.preis)+offset), start_zeit=elem.start_zeit).save()

def addTanken(start, end):
	random.seed()
	x = 0
	for i in range(start, (end+1)):
		x = random.uniform(-0.15, 0.15)
		x = float('%.2f' % x)
		addTankstellendaten(i, x)

def addTankstellenPreis():
	tanken = Tankstellen.objects.all()
	for elem in tanken:
		elem.preis = BenzinPreis.objects.all().filter(tankstelle = elem).order_by('start_zeit')[0].preis
		elem.save()
