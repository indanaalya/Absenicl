from rest_framework import serializers
from notulensi_app.models import Rapat, Absensi, Asisten

class AsistenSerializer(serializers.ModelSerializer):
  class Meta:
    model = Asisten
    fields = "__all__"

class AbsensiSerializer(serializers.ModelSerializer):

  class Meta:
    model = Absensi
    depth = 1
    fields = ['asisten', 'rapat', 'hadir']

class AbsensiPostSerializer(serializers.ModelSerializer):

  class Meta:
    model = Absensi
    fields = ['asisten', 'rapat', 'hadir']

class RapatSerializer(serializers.ModelSerializer):

  class Meta:
    model = Rapat
    fields = ['topik', 'notulensi']    

class DetailSerializer(serializers.Serializer):
  topik = serializers.CharField()
  notulensi = serializers.CharField()
  kehadiran = AbsensiSerializer(many = True)

class DetailAsisten(serializers.Serializer):
  asisten = AsistenSerializer()
  total_rapat = serializers.IntegerField()
  total_hadir = serializers.IntegerField()
  total_absen = serializers.IntegerField()

