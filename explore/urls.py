from django.contrib import admin
from django.urls import path
from explore.communities import views

urlpatterns = [
    # simple dashboard
    path('simple/', views.simple_dashboard),
    # simple dasboard with the input form
    path('input/', views.input_dashboard),
    # example with Pygal graphs
    path('plot/', views.plot_dashboard),
    # example with Jupyter Notebook
    path('notebook/', views.notebook),
    # "shiny dashboard"
    path('', views.shiny_dashboard),
    # admin panel
    path('admin/', admin.site.urls),
]
