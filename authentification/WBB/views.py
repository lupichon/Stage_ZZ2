from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
import WBB.scripts.main as w
from django.contrib import messages
import threading
from .models import GravityMeasurement

H = 0
W = 0

def wbb(request):
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
        if(w.board.status == "Disconnected"):
            update_thread = threading.Thread(target=w.main)
            update_thread.daemon = True  
            update_thread.start()
        
    return render(request,"WBB/wbb.html",context)




def get_point_position(request):
    if w.board.status == "Connected" :
        measurement = GravityMeasurement.objects.create(user=request.user,center_of_gravity_x = float(W)*w.x,center_of_gravity_y = float(H)*w.y)
        measurement.save()
        return JsonResponse({'x': w.x, 'y': w.y})
    else :
        return HttpResponseNotFound("Le tableau n'est pas connecté.")


