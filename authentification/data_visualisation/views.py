from django.shortcuts import render
from WBB.models import Data
import json
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.db.models import Max
from WBB.models import Data

def data_visualisation(request):
    lastID = Data.objects.filter(user=request.user).aggregate(Max('session_id'))['session_id__max']
    return render(request,"data_visualisation/main_page.html",{'lastID': lastID})

data = None
gravity_center = []
width = 0
height = 0
LEN = 0
ind = 0

acc = []


def get_visualisation(request):
    global data, gravity_center, width, height, LEN, ind, acc, ind_acc, LEN_ACC
    ind = 0
    ind_acc = 0
    if request.method == "POST" : 
        shotID = request.POST['shotID']
        sessionID = request.POST['sessionID']
    
    try : 
        data = Data.objects.get(user=request.user, session_id=sessionID, shot_id=shotID)

        gravity_center = data.gravity_center
        LEN = len(gravity_center)

        acc = data.acceleration
        LEN_ACC = len(acc)

        width = data.width
        height = data.height
        context = {
                'width' : data.width,
                'height' : data.height,
                'sessionID' : sessionID,
                'shotID' : shotID,
                }
        return render(request,"data_visualisation/visu.html",context)
    except : 
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

    
def visu_Acc(request):
    acc_X = []
    acc_Y = []
    acc_Z = []

    for elem in acc:
        acc_X.append(elem[0])
        acc_Y.append(elem[1])
        acc_Z.append(elem[2])

    return JsonResponse({'x': acc_X, 'y': acc_Y, 'z': acc_Z})


    
