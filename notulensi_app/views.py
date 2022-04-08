import json
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from notulensi_app.models import Rapat, Absensi, Asisten
from notulensi_app.serializers import (AsistenSerializer,
 AbsensiSerializer, 
 DetailSerializer, 
 RapatSerializer,
 DetailAsisten,
 AbsensiPostSerializer)
from django.shortcuts import render
from .models import Asisten, Rapat
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout

def login(request):
  return render(request,"login.html")

def performlogin(request):
  if request.method != "POST":
    return HttpResponse("Method not Allowed")
  else:
    print(request)
    username = request.POST.get('username')
    print(username)
    password = request.POST.get('password')
    print(username)
    userobj = authenticate(request, username=username,password=password)
    print(userobj)
    if userobj is not None:
      auth_login(request,userobj)
      messages.error(request,"Username atau Password salah !!!")
      return redirect("home")
    else:
      return redirect("login")

def coba(request):
  nama = "Tiara"
  a = 6
  b = 5
  luas_segitiga = a*b/2
  return render(request, 'coba.html',
  {
    "nama" : nama,
    "luas" : luas_segitiga,
  })

# Create your views here.
def home(request):
  asist = Asisten.objects.all()
  totalasis = len(asist)
  rapat = Rapat.objects.all()
  totalrapat = len(rapat)
  return render(request, 'index.html', { 
    "asisten" : asist,
    "totalasis" : totalasis,
    "rapat" : rapat,
    "totalrapat" : totalrapat,
  })

def asistenedit(request,nim):
  asist = Asisten.objects.filter(nim=nim)
  if request.method == "POST": 
    updatenama = request.POST["namaupdate"]
    updatenim  = request.POST["nimupdate"]
    delet = Asisten.objects.filter(nim=nim)
    delet.delete()
    update = Asisten(nim=updatenim, nama=updatenama)
    update.save()
    return redirect("tabelasisten")

  return render(request, "add-asisten.html", {
    "asisten" : asist,
  })

def asistendelete(request,nim):
  asist = Asisten.objects.filter(nim=nim)
  asist.delete()
  return redirect('tabelasisten')

def tabelrapat(request):
  if request.method == "POST":
    addjudul = request.POST["rapat"]
    addnotul = request.POST["notul"]

    addrapat = Rapat(topik=addjudul, notulensi=addnotul)
    addrapat.save()
    
    return HttpResponseRedirect("tablerapat.html")
  else: 
    rapat = Rapat.objects.all()
    asist = Asisten.objects.all()

  return render(request, 'tablerapat.html', {
    "rapat" : rapat,
    "asisten" : asist,    
  })

def addabsen(request):
  objrapat=Rapat.objects.all()
  objasisten = Asisten.objects.all()
  if request.method == "POST":
    addrapat = request.POST["rapat"]
    addnama = request.POST["nama"]
    addstatus = request.POST["status"]
    namarapat = Rapat.objects.filter(topik=addrapat)
    namaasisten = Asisten.objects.filter(nim=addnama)
    # cek = Absensi.objects.filter(asisten = addnama , rapat = addrapat)
    # print(cek)
    for item in namarapat:
      topikrapat = item
    for item in namaasisten:
      addnama = item
    cek = Absensi.objects.filter(asisten = addnama , rapat = topikrapat).exists()
    if cek == True :
      messages.success(request, "Data tidak terecord")
    else:
      absen = Absensi(rapat=topikrapat, asisten=addnama, hadir=addstatus)
      absen.save()
      return redirect('add-absensi')
  return render(request,"add-absensi.html",{
  "rapat" : objrapat,
  "asisten" : objasisten
  })

def rekaprapat(request):
  rapat = Rapat.objects.all()
  return render(request, 'rekaprapat.html',{
    "rapat" : rapat
  })

def rekapabsen(request):
  rapat = Rapat.objects.all()
  asist = Asisten.objects.all()
  return render(request, 'rekapabsen.html', {
    "rapat" : rapat,
    "asisten" : asist,
    })

def showabsenasisten(request):
  asisten = Asisten.objects.all()
  getnim = request.GET['rekapabsen']
  asistenobj = Absensi.objects.filter(asisten=getnim)

  for item in asistenobj:
    if item.hadir == True :
      item.hadir = "Hadir"
    else:
      item.hadir = "Absen"
  
 
  return render(request, "show-absensi.html",{
    "asisten":asisten,
    "objekterpilih" : asistenobj
  })

def show_rekap_rapat(request):
  rapat = Rapat.objects.all()
  getidrapat = request.GET['rapat']
  namarapat = Rapat.objects.get(id=getidrapat)
  print(namarapat)
  rapatobj = Absensi.objects.filter(rapat=getidrapat , hadir=True)

  for item in rapatobj:
    if item.hadir == True :
      item.hadir = "Hadir"
    else:
      item.hadir = "Absen"

  return render(request,"show-rekap-rapat.html",{
    "objekterpilih" : rapatobj,
    "rapat" : rapat,
    "nama_rapat" : namarapat
  })

def getabsensi(request,nim):
  asist = Asisten.objects.filter(nim=nim)
  if request.method == "GET":
    pass
  else :
    pass

def rekapabsennama(request,nim):
  pilih = Asisten.objects.filter(nim=nim)
  return render(request, "index.html" , {
    "pilih" : pilih
  })

def tabelasisten(request):
  if request.method == "POST":
    addnama= request.POST["nama"]
    addnim = request.POST["nim"]

    add_asisten = Asisten(nim=addnim, nama=addnama)
    add_asisten.save()
    return HttpResponseRedirect('tablesasisten.html')
  
  else:
    asist = Asisten.objects.all()

  return render(request, 'tablesasisten.html', {
    "asisten" : asist
  })



### INI UDAH API ###

class asisten_list(APIView):
  def get(self, request):
    asisten = Asisten.objects.all()
    serializer = AsistenSerializer(instance = asisten, many = True)
    return Response(serializer.data)
  
class rapat_list(APIView):

  def get(self, request):
    rapat = Rapat.objects.all()
    serializer = RapatSerializer(instance=rapat, many=True)
    return Response(serializer.data)

  def post(self, request):
    print(request.data)
    rapat_id = 0
    rapat_serializer = RapatSerializer(data = request.data['rapat'])

    if rapat_serializer.is_valid():
      rapat_new = rapat_serializer.save()
      rapat_id = rapat_new.id
    absensi = request.data['absensi']
    absensi_list = []

    all_asisten = Asisten.objects.all()

    for asisten in all_asisten:
      print(asisten)
      absensi_obj = {}
      absensi_obj["asisten"] = asisten.nim
      if asisten.nim in absensi:
        absensi_obj["hadir"] = False
      else:
        print(asisten.nim)
        absensi_obj["hadir"] = True
      absensi_obj["rapat"] = rapat_id
      absensi_list.append(absensi_obj)
    
    absensi_serializer = AbsensiPostSerializer(data = absensi_list, many = True)
    if absensi_serializer.is_valid():
      print("VALID")
      print(absensi_serializer.data)
      absensi_serializer.save()

    return Response({"status":"success"})

class absensi_list(APIView):

  def get(self, request):
    absensi = Absensi.objects.all()
    serializer = AbsensiSerializer(instance=absensi, many = True)
    return Response(serializer.data)
  
class hadir_list(APIView):

  def get(self, request, pk):
    data = {}

    rapat = Rapat.objects.get(pk = pk)
    absensi = Absensi.objects.filter(rapat__rapat=pk).filter(hadir = True)
    
    data["topik"] = rapat.topik
    data['notulensi'] = rapat.notulensi
    data['kehadiran'] = absensi
    serializer = DetailSerializer(data)
    return Response(data = serializer.data)

class tidak_hadir_list(APIView):
    def get(self, request, pk):
      data = {}

      rapat = Rapat.objects.get(pk = pk)
      absensi = Absensi.objects.filter(rapat__rapat=pk).filter(hadir = False)
      
      data["topik"] = rapat.topik
      data['notulensi'] = rapat.notulensi
      data['kehadiran'] = absensi
      serializer = DetailSerializer(data)
      return Response(data = serializer.data)

class detail_asisten(APIView):
  def get(self, request, nim):
    data = {}
    total_rapat = len(Rapat.objects.all())
    total_hadir = len(Absensi.objects.filter(asisten__nim=nim).filter(hadir = True))
    print(total_hadir)
    total_absen = total_rapat - total_hadir
    asisten = Asisten.objects.get(nim = nim)
    data['asisten'] = asisten
    data['total_hadir'] = total_hadir
    data['total_rapat'] = total_rapat
    data['total_absen'] = total_absen

    serializer = DetailAsisten(data)
    return Response(data = serializer.data)

