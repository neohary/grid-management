from django.urls import path, include
from rest_framework.routers import DefaultRouter

from grid import views

router = DefaultRouter()
router.register('village',views.VillageViewSet,basename='village')
router.register('mgrid',views.MicroGridViewSet,basename='mgrid')
router.register('stemplate',views.sTemplateViewSet,basename='stemplate')
router.register('sinstance',views.sInstanceViewSet,basename='sinstance')

urlpatterns = [
    #path('',include(router.urls)),
]