from django.urls import path

from . import views

app_name = "tareas"
urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("guardar_tarea/", views.guardar_tarea, name="guardar_tarea"),
    path("post_guardar/", views.post_guardar, name="post_guardar"),
    #path("<int:tarea_id>/", views.tarea_info, name="tarea_info")
]

