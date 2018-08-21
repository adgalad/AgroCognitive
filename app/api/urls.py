from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

import app.api.views as views

urlpatterns = [

    url(r'^auth/', obtain_jwt_token),
    url(r'^auth/refresh/', refresh_jwt_token),
    url(r'^auth/verify/', verify_jwt_token),

    url(r'^users/$', views.UserAPI.as_view(), name='user-listcreate'),
    url(r'^user/(?P<pk>\d+)/$', views.UserRud.as_view(), name='user-rud'),

    url(r'^payments/$', views.PaymentAPI.as_view(), name='payment-listcreate'),
    url(r'^payment/(?P<pk>\d+)/$', views.PaymentRud.as_view(), name='payment-rud'),

    url(r'^crops/$', views.CropAPI.as_view(), name='crop-listcreate'),
    url(r'^crop/(?P<pk>\d+)/$', views.CropRud.as_view(), name='crop-rud'),

    url(r'^terrains/$', views.TerrainAPI.as_view(), name='terrain-listcreate'),
    url(r'^terrain/(?P<pk>\d+)/$', views.TerrainRud.as_view(), name='terrain-rud'),

    url(r'^companies/$', views.CompanyAPI.as_view(), name='company-listcreate'),
    url(r'^company/(?P<pk>\d+)/$', views.CompanyRud.as_view(), name='company-rud'),

    url(r'^diagnostics/$', views.DiagnosticAPI.as_view(), name='diagnostic-listcreate'),
    url(r'^diagnostic/(?P<pk>\w+)/$', views.DiagnosticRud.as_view(), name='diagnostic-rud'),

    url(r'^affections/$', views.AffectionAPI.as_view(), name='affection-listcreate'),
    url(r'^affection/(?P<pk>\w+)/$', views.AffectionRud.as_view(), name='affection-rud'),

    url(r'^fumigationTypes/$', views.FumigationTypeAPI.as_view(), name='fumigationType-listcreate'),
    url(r'^fumigationType/(?P<pk>\w+)/$', views.FumigationTypeRud.as_view(), name='fumigationType-rud'),
    
    url(r'^nutritionTypes/$', views.NutritionTypeAPI.as_view(), name='nutritionType-listcreate'),
    url(r'^nutritionType/(?P<pk>\w+)/$', views.NutritionTypeRud.as_view(), name='nutritionType-rud'),
    
    url(r'^prunMethods/$', views.PrunMethodAPI.as_view(), name='prunMethod-listcreate'),
    url(r'^prunMethod/(?P<pk>\w+)/$', views.PrunMethodRud.as_view(), name='prunMethod-rud'),
    
    url(r'^irrigationMethods/$', views.IrrigationMethodAPI.as_view(), name='irrigationMethod-listcreate'),
    url(r'^irrigationMethod/(?P<pk>\w+)/$', views.IrrigationMethodRud.as_view(), name='irrigationMethod-rud'),

    url(r'^activities/$', views.ActivityAPI.as_view(), name='activity-listcreate'),
    url(r'^activity/(?P<pk>\w+)/$', views.ActivityRud.as_view(), name='activity-rud'),

    url(r'^measures/$', views.MeasureAPI.as_view(), name='measure-listcreate'),
    url(r'^measure/(?P<pk>\w+)/$', views.MeasureRud.as_view(), name='measure-rud'),


    url(r'^uploadImages/$', csrf_exempt(views.uploadImages.as_view()), name="uploadImages")
]   