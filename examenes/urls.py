from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.examenes_list, name='examenes_list'),
    url(r'^(?P<examen_id>[0-9]+)/$', views.examen_detail, name='detail'),
    url(r'^credits/', views.credits_page, name='credits'),
    url(r'^solucion_examen/', views.check_examen, name='check_examen'),
]
