from django.contrib import admin
from models import Tankstellen, FahrtDaten, UserPositions, BenzinPreis

class UserView(admin.ModelAdmin):
	fields = ('zeit', 'benzin_delta_in_l', 'position_x', 'position_y')

admin.site.register(Tankstellen)
admin.site.register(FahrtDaten)
admin.site.register(UserPositions, UserView)
admin.site.register(BenzinPreis)

# Register your models here.
