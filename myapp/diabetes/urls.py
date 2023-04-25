from django.urls import path
from diabetes import views

urlpatterns = [
    path('', views.welcome_action, name='welcome'),
    path('about', views.about_action, name='about'),
    path('newrecord', views.new_record_action, name='new_record'),
    path('predict', views.predict_action, name='predict'),
    path('statistics', views.statistics_action, name='statistics'),
]