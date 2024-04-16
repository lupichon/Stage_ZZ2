from django.urls import path
from WBB import views

urlpatterns = [
    path("wbb",views.wbb,name = "wbb"),
    path("connectMicrophone",views.connectMicrophone,name="connectMicrophone"),
    path("connectWiiboard",views.connectWiiboard,name="connectWiiboard"),
    path("get_point_position",views.get_point_position,name = "get_point_position"),
    path("sort_data",views.sort_data,name = "sort_data"),
]