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
from django.db.models import Max

H = 0
W = 0

new_session = True
shot_id = 1
session_id = None
first_connexion = True

def wbb(request):
    global H, W, session_id, new_session, first_connexion

    if w.board.status == "Connected" and m.reader.connected==True:
        if first_connexion : 
            session_id = Data.objects.filter(user=request.user).aggregate(Max('session_id'))['session_id__max']
            first_connexion = False

        if session_id is None :
            session_id = 0
        
        if new_session : 
            session_id = session_id + 1
            new_session = False
        
        context={}
        if request.method == "POST" : 
            hauteur = request.POST['height']
            largeur = request.POST['width']
            context = {
                'width' : largeur,
                'height' : hauteur,
                'sessionID' : session_id,
                'shotID' : shot_id,
            }
            H = context['height']
            W = context['width']
        if hauteur!="" and largeur!="" :
            return render(request,"WBB/wbb.html",context)
        else:
            messages.error(request,"Please, entry the height and the width")
            return render(request,"app/index.html")
    
    else:
        messages.error(request, "The sensors and the wiiboard must be connected before start")
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
        messages.error(request,"The sensors are already connected")
        return render(request,"app/index.html")
   
LEN_GC = 100
measure_gc = [[0,0] for _ in range(LEN_GC)]
data_gc = []
after_gc = False
ind_gc = 0
OK_GC = False

LEN_ACC = 100
measure_acc = [[0,0,0] for _ in range(LEN_ACC)]
data_acc = []
after_acc = False
ind_acc = 0
OK_ACC = False

ENABLE = False
time_before = 0

def get_point_position(request):
    global OK_ACC, OK_GC, data_gc, data_acc, ENABLE, time_before, session_id, shot_id
    if w.board.status == "Connected" and m.reader.connected == True:
        ENABLE = m.trigger
        m.trigger = False
        saveGravityCenter()
        saveAcc()
        if(OK_ACC and OK_GC and time.time() - time_before>10):
            time_before = time.time()
            measurement = Data.objects.create(user=request.user,session_id = session_id, shot_id = shot_id, gravity_center = data_gc, acceleration = data_acc, height=float(H), width=float(W))
            measurement.save()
            shot_id = shot_id + 1
            data_gc = []
            data_acc = []
            OK_ACC = False
            OK_GC = False

        return JsonResponse({'x': w.x, 'y': w.y, 'acc_x' : m.acceleration_x, 'acc_y' : m.acceleration_y, 'acc_z' : m.acceleration_z, 'sessionID' : session_id, 'shotID': shot_id})
    else:
        return HttpResponseNotFound("error")
    
def saveGravityCenter():
    global measure_gc, after_gc, ind_gc, data_gc, OK_GC

    measure_gc.pop(0)
    measure_gc.append([float(W) * w.x / 2, float(H) * w.y / 2])
    if after_gc == True and ind_gc<LEN_GC: 
        data_gc.append([measure_gc[LEN_GC-1][0],measure_gc[LEN_GC-1][1]])
        ind_gc = ind_gc +1
        if(ind_gc==LEN_GC-1) : 
            ind_gc=0
            after_gc=False
            OK_GC = True
    else : 
        if ENABLE==True and after_gc == False and OK_GC == False:
            data_gc = copy.deepcopy(measure_gc)
            after_gc = True

def saveAcc():
    global measure_acc, after_acc, ind_acc, data_acc, OK_ACC

    measure_acc.pop(0)
    measure_acc.append([m.acceleration_x,m.acceleration_y,m.acceleration_z])

    if after_acc == True and ind_acc<LEN_ACC: 
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
    global new_session, shot_id
    shot_id = 1
    m.finish = True
    w.running = False
    messages.success(request,"Measures finished")
    new_session = True
    return render(request,"app/index.html")

