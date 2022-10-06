from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core import views

router = DefaultRouter()
router.register('user',views.UserViewSet,basename='user')
router.register('group',views.GroupViewSet,basename='group')
router.register('user-approval',views.UserApprovalViewSet,basename='user-approval')

urlpatterns = [
    #path('',include(router.urls)),
    
]