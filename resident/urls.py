from django.urls import path, include
from rest_framework.routers import DefaultRouter

from resident import views

router = DefaultRouter()
#router.register('resident',views.ResidentViewSet)
router.register('residents',views.ResidentViewSet,basename='resident')
router.register('houses',views.HouseViewSet,basename='house')

urlpatterns = [
    #path('',include(router.urls)),
]