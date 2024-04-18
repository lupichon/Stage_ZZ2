from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
import WBB.scripts.main as w
import WBB.scripts.dataSensors as m
from django.contrib import messages
import threading
from .models import Data
from datetime import timedelta
from django.utils import timezone
import copy
import time

H = 0
W = 0

def wbb(request):
    if w.board.status == "Connected" and m.reader.connected==True:
        Data.objects.all().delete()
        
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

def connectSensors(request):
    if(m.reader.connected == False):
        m.finish = False
        Sensors_thread = threading.Thread(target=m.main)
        Sensors_thread.daemon = True  
        Sensors_thread.start()

        while m.reader.connected == False and m.find == True:
            pass

        if m.reader.connected == False:
            messages.error(request, "Microphone and accelerometer not connected, please try again")
        else : 
            messages.success(request, "Microphone and accelerometer connected")
    
        m.find = True
        return render(request,"app/index.html")
    
    else:
        m.find = True
        messages.error(request,"The microphone is already connected")
        return render(request,"app/index.html")
   
LEN = 30
measure_gc = [[0,0] for _ in range(LEN)]
data = []
after = False
i = 0

LEN_ACC = 30
measure_acc = [[0,0,0] for _ in range(LEN_ACC)]
data_acc = []
after_acc = False
ind_acc = 0

OK_ACC = False
OK_GC = False

ENABLE = False
time_before = 0

def get_point_position(request):
    global OK_ACC, OK_GC, data, data_acc, ENABLE, time_before
    if w.board.status == "Connected" and m.reader.connected == True:
        ENABLE = m.trigger
        m.trigger = False
        saveGravityCenter()
        saveAcc()
        if(OK_ACC and OK_GC and time.time() - time_before>5):
            time_before = time.time()
            measurement = Data.objects.create(user=request.user,gravity_center = data, acceleration = data_acc)
            measurement.save()
            data = []
            data_acc = []
            OK_ACC = False
            OK_GC = False

        return JsonResponse({'x': w.x, 'y': w.y})
    else:
        return HttpResponseNotFound("error")
    
def saveGravityCenter():
    global measure_gc, after, i, data, OK_GC

    measure_gc.pop(0)
    measure_gc.append([float(W) * w.x / 2, -1 * float(H) * w.y / 2])
    if after == True and i<LEN: 
        data.append([measure_gc[LEN-1][0],measure_gc[LEN-1][1]])
        i = i +1
        if(i==LEN-1) : 
            i=0
            after=False
            OK_GC = True
    else : 
        if ENABLE==True and after == False and OK_GC == False:
            data = copy.deepcopy(measure_gc)
            after = True

def saveAcc():
    global measure_acc, after_acc, ind_acc, data_acc, OK_ACC

    measure_acc.pop(0)
    measure_acc.append([m.acceleration_x,m.acceleration_y,m.acceleration_z])

    if after_acc == True and i<LEN_ACC: 
        data_acc.append([measure_acc[LEN_ACC-1][0],measure_acc[LEN_ACC-1][1],measure_acc[LEN_ACC-1][2]])
        ind_acc = ind_acc +1

        if(ind_acc==LEN_ACC-1) : 
            ind_acc = 0
            after_acc =False
            OK_ACC = True
    else : 
        if ENABLE ==True and after_acc == False and OK_ACC == False:
            data_acc = copy.deepcopy(measure_acc)
            after_acc = True



def finish(request):
    m.finish = True
    w.running = False
    messages.success(request,"Measures finished")
    return render(request,"app/index.html")