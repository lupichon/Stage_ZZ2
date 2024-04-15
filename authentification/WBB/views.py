from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
import WBB.scripts.main as w
import WBB.scripts.dataMicrophone as m
from django.contrib import messages
import threading
from .models import GravityMeasurement
import time

H = 0
W = 0

def wbb(request):
    if w.board.status == "Connected" and m.reader.connected==True:
        GravityMeasurement.objects.all().delete()
        global H, W
        context={}
        if request.method == "POST" : 
            hauteur = request.POST['height']
            largeur = request.POST['width']
            context = {
                'width' : largeur,
                'height' : hauteur,
            }
            H = context['height']
            W = context['width']
        if hauteur!="" and largeur!="" :
            return render(request,"WBB/wbb.html",context)
        else:
            messages.error(request,"Please, entry the height and the width")
            return render(request,"app/index.html")
    
    else:
        messages.error(request, "The microphone and the wiiboard must be connected before start")
        return render(request,"app/index.html")
    
def connectWiiboard(request):
    if(w.board.status == "Disconnected"):
        Wiiboard_thread = threading.Thread(target=w.main)
        Wiiboard_thread.daemon = True  
        Wiiboard_thread.start()

        while w.board.status!="Connected" and w.find == True:
            pass

        if w.board.status == "Disconnected":
            messages.error(request,"Wiiboard not connected, please try again")
        else : 
            messages.success(request, "Wiiboard connected")

        w.find = True
        return render(request,"app/index.html")
    
    else : 
        w.find = True
        messages.error(request,"The Wiiboard is already connected")
        return render(request,"app/index.html")

def connectMicrophone(request):
    if(m.reader.connected == False):
        Sensors_thread = threading.Thread(target=m.main)
        Sensors_thread.daemon = True  
        Sensors_thread.start()

        while m.reader.connected == False and m.find == True:
            pass

        if m.reader.connected == False:
            messages.error(request, "Microphone not connected, please try again")
        else : 
            messages.success(request, "Microphone connected")
    
        m.find = True
        return render(request,"app/index.html")
    
    else:
        m.find = True
        messages.error(request,"The microphone is already connected")
        return render(request,"app/index.html")
   


def get_point_position(request):
    if w.board.status == "Connected" and m.reader.connected == True:
        if m.trigger == 1:
            measurement = GravityMeasurement.objects.create(user=request.user,center_of_gravity_x = float(W)*w.x/2,center_of_gravity_y = -1*float(H)*w.y/2, sound = m.data_microphone)
            measurement.save()
            m.trigger = 0
        return JsonResponse({'x': w.x, 'y': w.y})
    else :
        return HttpResponseNotFound("Le tableau n'est pas connecté.")


