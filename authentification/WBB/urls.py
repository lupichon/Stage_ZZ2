from django.urls import path
from WBB import views

urlpatterns = [
    path("wbb",views.wbb,name = "wbb"),
    path("get_point_position",views.get_point_position,name = "get_point_position"),
]