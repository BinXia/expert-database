from django.conf.urls import url
from info import views

urlpatterns = [
    url(r'^PullComboInfo', views.PullComboInfo, name='PullComboInfo'),
    url(r'^ShowExpertList', views.ShowExpertList, name='ShowExpertList'),
    url(r'^InsertDatum', views.InsertDatum, name='InsertDatum'),
    url(r'^CorrectDatum', views.CorrectDatum, name='CorrectDatum'),
    url(r'^DeleteDatum', views.DeleteDatum, name='DeleteDatum'),
]