from django.conf.urls import url
from info import views

urlpatterns = [
    url(r'^PullComboInfo', views.PullComboInfo, name='PullComboInfo'),
    url(r'^ShowExpertList', views.ShowExpertList, name='ShowExpertList'),

]