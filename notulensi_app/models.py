from django.db import models

# Create your models here.
class Asisten(models.Model):
  nim = models.CharField(max_length=30, primary_key=True, null=False) 
  nama = models.CharField(max_length=100)
  def __str__(self):
    return self.nama


class Rapat(models.Model):
  topik = models.CharField(max_length=50)
  notulensi = models.TextField()

  def __str__(self):
    return self.topik

class Absensi(models.Model):
   rapat = models.ForeignKey(Rapat, related_name='rapat', on_delete=models.CASCADE)
   asisten = models.ForeignKey(Asisten, related_name='asisten', on_delete=models.CASCADE)
   hadir = models.BooleanField()