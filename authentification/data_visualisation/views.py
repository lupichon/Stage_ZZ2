from django.shortcuts import render
from WBB.models import Data
import json
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.db.models import Max
from WBB.models import Data
import socket
import struct
import subprocess
import time
import WBB.scripts.dataSensors as m

HOST = '127.0.0.1'
PORT = 12345

process = None

def data_visualisation(request):
    lastID = Data.objects.filter(user=request.user).aggregate(Max('session_id'))['session_id__max']
    return render(request,"data_visualisation/main_page.html",{'lastID': lastID})

data = None
gravity_center = []
width = 0
height = 0
LEN = 0
ind = 0

qua = []
LEN_QUA = 0
LEN_QUA_DIV2 = 0
ind_qua = 0

processing_socket = None


def get_visualisation(request):
    global data, gravity_center, width, height, LEN, ind, qua, ind_qua, LEN_QUA, LEN_QUA_DIV2, processing_socket, process
    ind = 0
    ind_qua = 0

    processing_java_path = "/home/lucas/Downloads/processing-4.3-linux-x64/processing-4.3/processing-java"
    sketch_directory = "/home/lucas/ISIMA/Stage/Wii/Stage_ZZ2/Sensors/visualisation/visu_rifle"
    command = [processing_java_path, "--sketch=" + sketch_directory, "--run"]

    if request.method == "POST" : 
        shotID = request.POST['shotID']
        sessionID = request.POST['sessionID']
    
    try : 
        
        if m.reader.connect_processing == True : 
            m.visualisation = True
        
        else : 
            if process is None or process.poll() is not None: 
                process = subprocess.Popen(command)
                time.sleep(7)

        processing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        processing_socket.connect((HOST, PORT))

        data = Data.objects.get(user=request.user, session_id=sessionID, shot_id=shotID)

        gravity_center = data.gravity_center
        LEN = len(gravity_center)

        qua = data.quaternion
        LEN_QUA = len(qua)
        LEN_QUA_DIV2 = LEN_QUA//2

        width = data.width
        height = data.height
        context = {
                'width' : data.width,
                'height' : data.height,
                'sessionID' : sessionID,
                'shotID' : shotID,
                }
        
        return render(request,"data_visualisation/visu.html",context)
    except Exception as e: 
        print(str(e))
        messages.error(request,"The session ID and the shot ID do not match")
        return render(request,"data_visualisation/main_page.html")


def visu_gravityCenter(request):
    global ind
    if ind<LEN:
        ind = ind + 1
        if ind-1 == LEN//2 :
            return JsonResponse({'x': gravity_center[ind-1][0], 'y': gravity_center[ind-1][1], 'width': width, 'height': height,'status': 0})
        else:
            return JsonResponse({'x': gravity_center[ind-1][0], 'y': gravity_center[ind-1][1], 'width': width, 'height': height,'status': 1})
    else:
        ind = 0
        return JsonResponse({'x': 0, 'y': 0, 'width': width, 'height': height,'status': 2})

def visu_rifle(request):
    global ind_qua
    if ind_qua < LEN_QUA:
        ind_qua = ind_qua + 1

        q0 = bytearray(struct.pack("f", qua[ind_qua-1][0]))
        q1 = bytearray(struct.pack("f", qua[ind_qua-1][1]))
        q2 = bytearray(struct.pack("f", qua[ind_qua-1][2]))
        q3 = bytearray(struct.pack("f", qua[ind_qua-1][3]))
        shot = b'0'
        
        if ind_qua > LEN_QUA_DIV2-20 and ind_qua < LEN_QUA_DIV2+20: 
            shot = b'1'

        data = q0 + q1 + q2 + q3 + shot
        
        try : 
            processing_socket.sendall(data)
        except : 
            pass

    else:
        ind_qua = 0

    return JsonResponse({})


def visu_Acc(request):
    acc_X = []
    acc_Y = []
    acc_Z = []

    for elem in acc:
        acc_X.append(elem[0])
        acc_Y.append(elem[1])
        acc_Z.append(elem[2])

    return JsonResponse({'x': acc_X, 'y': acc_Y, 'z': acc_Z})
