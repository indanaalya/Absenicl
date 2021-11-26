from django.contrib import admin
from notulensi_app.models import Rapat, Absensi, Asisten

# Register your models here.
admin.site.register(Rapat)
admin.site.register(Absensi)
admin.site.register(Asisten)