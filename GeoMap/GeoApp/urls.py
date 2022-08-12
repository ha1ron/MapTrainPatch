from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

    path('', views.main, name='main'),
    path('proto', views.home, name='proto'),
    path('map', views.map, name='map'),
    path('map_two', views.map_two, name='map_two'),
    path('map_uno', views.map_uno, name='map_uno'),

    path('map_ajax', views.map_ajax, name='map_ajax'), #ajax
    path('map_uno_ajax', views.map_uno_ajax, name='map_uno_ajax'), #ajax
    path('poezd_suggest', views.poezd_suggest, name='poezd_suggest') #ajax
    # path('odata', views.oData, name='odata'),
    # path('no_data', views.oData, name='no_data'),

]
