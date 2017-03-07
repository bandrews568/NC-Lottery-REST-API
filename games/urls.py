from games import views

from django.conf.urls import url

urlpatterns = [
    url(r'^all/$', views.all_games),
    url(r'^pick3/$', views.pick3),
    url(r'^pick4/$', views.pick4),
    url(r'^cash5/$', views.cash5),
    url(r'^powerball/$', views.powerball),
    url(r'^megamillions/$', views.mega_millions),
    url(r'^luckyforlife/$', views.lucky_for_life),
]
