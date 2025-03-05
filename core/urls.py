from django.urls import path
from core.views import index
from core import views

app_name = "core"

urlpatterns = [
    # path("ceva/", views.index), 
    path("", index, name="index"),
    # Here I'm telling it where to put that =)) beaware of the paths!
]
