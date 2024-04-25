from django.urls import path
from WBB import views

urlpatterns = [
    path("wbb",views.wbb,name = "wbb"),
    path("connectSensors",views.connectSensors,name="connectSensors"),
    path("connectWiiboard",views.connectWiiboard,name="connectWiiboard"),
    path("get_point_position",views.get_point_position,name = "get_point_position"),
    path("get_Acc", views.get_Acc, name = "get_Acc"),
    path("save", views.save_Measure, name="save"),
    path("finish",views.finish,name = "finish"),
]