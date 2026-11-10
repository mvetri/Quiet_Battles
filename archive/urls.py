from django.urls import path
from . import views

urlpatterns = [
    path('', views.archive, name='archive'),

    path(
        'chapter/<slug:slug>/',
        views.chapter_detail,
        name='chapter_detail'
    ),
]