from django.urls import path
from core import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('snap', views.snap, name='snap'),
    path('location/<str:snap_url>', views.location, name='location'),
    path('result/<str:photo_url>', views.result, name='result'),
    path('editor/<str:snap_url>/<str:location_title>', views.editor, name='editor'),
    path('save_image', views.save_image, name='save_image'),
    path('save_snap', views.save_snap, name='save_snap')
]
