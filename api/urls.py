from django.urls import path, include
from rest_framework.routers import DefaultRouter,SimpleRouter
from resident.urls import router as resident_router
from grid.urls import router as grid_router
from index.urls import router as index_router
from core.urls import router as core_router

from grid_management import settings

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.registry.extend(resident_router.registry)
router.registry.extend(grid_router.registry)
router.registry.extend(index_router.registry)
router.registry.extend(core_router.registry)

from core import views as core_views

urlpatterns = [
    path('',include(router.urls)),
    path('user-register/',core_views.CreateUserView.as_view(),name='user-register'),
    path('login/',core_views.LoginView.as_view(),name='api-login-view'),
    path('logout/',core_views.LogoutView.as_view(),name='api-logout-view'),
]