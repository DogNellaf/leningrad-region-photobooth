from django.urls import path
from core import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('snap', views.snap, name='snap'),
    path('location', views.location, name='location'),
    path('result', views.result, name='result')
]
