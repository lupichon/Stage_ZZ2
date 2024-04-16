from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
import WBB.scripts.main as w
import WBB.scripts.dataMicrophone as m
from django.contrib import messages
import threading
from .models import GravityMeasurement
from .models import Data
from datetime import timedelta
from django.utils import timezone
import copy

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
   
LEN = 30
measure = [[0,0] for _ in range(LEN)]
data = []
after = False
i = 0

def get_point_position(request):
    global measure, after, i, data
    if w.board.status == "Connected" and m.reader.connected == True:
        measure.pop(0)
        measure.append([float(W) * w.x / 2, -1 * float(H) * w.y / 2])
        if after == True and i<LEN: 
            data.append([measure[LEN-1][0],measure[LEN-1][1]])
            i = i +1
            if(i==29) : 
                i=0
                after=False
                measurement = GravityMeasurement.objects.create(user=request.user,shot = data)
                measurement.save()
                data = []
        else : 
            if m.trigger==True and after == False:
                data = copy.deepcopy(measure)
                after = True
                m.trigger = False
        return JsonResponse({'x': w.x, 'y': w.y})
    else:
        return HttpResponseNotFound("Le tableau n'est pas connecté.")








def sort_data(request):
    #elem = GravityMeasurement.objects.all()
    elem = list(GravityMeasurement.objects.all())
    for element in elem : 
        if element.sound > 1000 : 
            range = timedelta(seconds=5)
            start_time = element.measurement_date - range
            end_time = element.measurement_date + range

            elements_before = GravityMeasurement.objects.filter(measurement_date__gte=start_time, measurement_date__lt=element.measurement_date)
            elements_after = GravityMeasurement.objects.filter(measurement_date__gt=element.measurement_date, measurement_date__lte=end_time)

            values = []

            for e in elements_before : 
                values.append([e.center_of_gravity_x,e.center_of_gravity_y])
                elem.remove(e)

            values.append([element.center_of_gravity_x, element.center_of_gravity_y])
            elem.remove(values)

            for e in elements_after : 
                values.append([e.center_of_gravity_x,e.center_of_gravity_y])
                elem.remove(e)

            data = Data.objects.create(user=request.user,shot=values)
            data.save()
    return render(request,"app/index.html")
    