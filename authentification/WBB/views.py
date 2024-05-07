from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpRequest
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
import subprocess
import os
import signal

H = 0
W = 0

new_session = True
shot_id = 1
session_id = None
first_connexion = True

def wbb(request):
    global H, W, session_id, new_session, first_connexion
        
    processing_java_path = "/home/lucas/Downloads/processing-4.3-linux-x64/processing-4.3/processing-java"
    sketch_directory = "/home/lucas/ISIMA/Stage/Wii/Stage_ZZ2/Sensors/visualisation/visu_rifle"
    command = [processing_java_path, "--sketch=" + sketch_directory, "--run"]
    
    if w.board.status == "Connected" and m.reader.connected==True:

        m.visualisation = False
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
            m.trigger = False

            if m.reader.connect_processing == False : 
                subprocess.Popen(command)
            
            '''chemin_relatif = "../../Sensors/visualisation/visu_rifle/linux-amd64/visu_rifle"
            chemin_absolu = os.path.dirname(os.path.abspath(__file__))
            chemin_absolu_exe = os.path.join(chemin_absolu, chemin_relatif)
            subprocess.Popen([chemin_absolu_exe])'''
            
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
   
LEN_GC = 30
before_gc = True
measure_gc_after = []
measure_gc_before = [[0,0] for _ in range(LEN_GC)]
ind_gc = 0

LEN_ACC = 100
before_acc = True
measure_acc_after = []
measure_acc_before = [[0,0,0] for _ in range(LEN_ACC)]
ind_acc = 0

LEN_QUA = 150
before_qua = True
measure_qua_after = []
measure_qua_before = [[0,0,0,0] for _ in range(LEN_QUA)]
ind_qua = 0

def get_point_position(request):
    global ind_gc
    X = w.x 
    Y = w.y 
    CoG = m.CoG
    m.CoG = 0

    if before_gc : 
        measure_gc_before.pop(0)
        measure_gc_before.append([float(W) * X / 2, float(H) * Y / 2])
        ind_gc = 0
    
    else :
        if ind_gc < LEN_GC :
            measure_gc_after.append([float(W) * X / 2, float(H) * Y / 2])
            ind_gc = ind_gc + 1

    return JsonResponse({'x': X, 'y': Y, 'sessionID': session_id, 'shotID': shot_id, 'CoG': CoG})

def get_Acc(request):
    global ind_acc

    Ax = m.acceleration_x
    Ay = m.acceleration_y
    Az = m.acceleration_z

    if before_acc : 
        measure_acc_before.pop(0)
        measure_acc_before.append([Ax,Ay,Az])
        ind_acc = 0

    else:
        if ind_acc < LEN_ACC:
            measure_acc_after.append([Ax,Ay,Az])
            ind_acc = ind_acc + 1

    return JsonResponse({'acc_x' : Ax, 'acc_y' : Ay, 'acc_z' : Az})

def get_Quaternion(request):
    global ind_qua

    q0 = m.q0
    q1 = m.q1
    q2 = m.q2
    q3 = m.q3

    if before_qua : 
        measure_qua_before.pop(0)
        measure_qua_before.append([q0,q1,q2,q3])
        ind_qua = 0

    else:
        if ind_qua < LEN_QUA:
            measure_qua_after.append([q0,q1,q2,q3])
            ind_qua = ind_qua +1

    return JsonResponse({})

def save_Measure(request):
    global measure_gc_before, shot_id, session_id, H, W, before_gc, measure_gc_after, measure_qua_after, measure_qua_before, before_qua
    if m.trigger: 
        m.trigger = False
        shot_id = shot_id + 1

        data_gc = copy.deepcopy(measure_gc_before)
        data_qua = copy.deepcopy(measure_qua_before)

        before_gc = False
        before_qua = False

        while (len(measure_gc_after) < LEN_GC or len(measure_qua_after) < LEN_QUA) :
            pass

        if len(measure_gc_after) == LEN_GC : 
            before_gc = True
            data_gc = data_gc + measure_gc_after
            measure_gc_after = []

            while len(measure_qua_after) < LEN_QUA:
                pass

            before_qua = True
            data_qua = data_qua + measure_qua_after
            measure_qua_after = []

        elif len(measure_qua_after) == LEN_QUA:
            before_qua = True
            data_qua = data_qua + measure_qua_after
            measure_qua_after = []

            while len(measure_gc_after) < LEN_GC : 
                pass
            
            before_gc = True
            data_gc = data_gc + measure_gc_after
            measure_gc_after = []
            
        
        #measurement = Data.objects.create(user=request.user,session_id = session_id, shot_id = shot_id, gravity_center = data_gc, acceleration = data_acc, height=float(H), width=float(W))
        measurement = Data.objects.create(user=request.user,session_id = session_id, shot_id = shot_id, gravity_center = data_gc, quaternion = data_qua, height=float(H), width=float(W))
        measurement.save()

    return JsonResponse({})
    

def finish(request):
    global new_session, shot_id
    shot_id = 1
    m.finish = True
    w.running = False
    messages.success(request,"Measures finished")
    new_session = True
    return render(request,"app/index.html")