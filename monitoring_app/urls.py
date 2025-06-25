from django.urls import path
from . import views

app_name='monitoring_app'

urlpatterns = [ 
   path('current-metrics/', views.retrieve_and_save_metrics, name='current_metrics'),
   path('compare-metrics/', views.compare_metrics_view, name='compare_metrics')
]