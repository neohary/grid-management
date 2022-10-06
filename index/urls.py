from django.urls import path, include
from rest_framework.routers import DefaultRouter

from index import views
import notifications.urls

router = DefaultRouter()
router.register('resident-logs',views.ResidentChangeLogViewSet,basename='residentLogs')
router.register('house-logs',views.HouseChangeLogViewSet,basename='houseLogs')
router.register('village-logs',views.VillageChangeLogViewSet,basename='villageLogs')
router.register('mgrid-logs',views.MicroGridChangeLogViewSet,basename='mgridLogs')
router.register('stemplate-logs',views.CustomStaticsTemplateChangeLogViewSet,basename='sTemplateLogs')
router.register('sinstance-logs',views.CustomStaticsInstanceChangeLogViewSet,basename='sInstanceLogs')

urlpatterns = [
    path('',views.index,name='index'),
    path('map/',views.map,name='map'),
    path('residents/list',views.residentList,name='resident-list-html'),
    path('resident/<int:pk>',views.residentDetail,name='resident-detail-html'),
    path('houses/list',views.houseList,name='house-list-html'),
    path('house/<int:pk>',views.houseDetail,name='house-detail-html'),
    path('grids/list',views.mgridList,name='grid-list-html'),
    path('grid/<int:pk>',views.mgridDetail,name='grid-detail-html'),
    path('statistics/list',views.cStaticList,name='static-list-html'),
    path('statistics/create',views.cStaticCreate,name='static-create-html'),
    path('statistics/<int:pk>',views.cStaticDetail,name='static-detail-html'),
    path('login/',views.userLogin,name='user-login-html'),
    path('logout/',views.userLogout,name='user-logout-html'),
    path('user/list',views.userList,name='user-list-html'),
    path('user/<int:pk>',views.userDetail,name='user-detail-html'),
    path('user/register',views.userRegister,name='user-register-html'),
    path('user/reset_password',views.userResetPassword,name='user-reset-password-html'),
    path('user/register/complete/',views.userRegistSuccess,name='user-regist-complete-html'),
    path('select-village/',views.villageSelect,name='select-village-html'),
    path('select-village/<int:pk>',views.villageSelectDetail,name='select-village-detail-html'),
    path('select-village/complete/',views.villageSelectSuccess,name='select-village-complete-html'),
    path('user-approval/list',views.userApprovalList,name='user-approval-list-html'),
    path('user/<int:pk>/edit-user-group',views.editUserGroup,name='user-edit-group-html'),
    path('village/create-complete',views.village_create_complete,name='village-create-complete-html'),
    path('village/list',views.village_list,name='village-list-html'),
    path('village/<int:pk>',views.village_detail,name='village-detail-html')
]

urlpatterns += [
    path('inbox/notifications/',include(notifications.urls),name='notifications'),
    path('notify/test/',views.NotifyTest,name='nofity-test'),
    path('notify/list/',views.NoticeListView.as_view(),name='notify-list-html'),
    path('notify/mark-all-as-read/',views.notify_mark_all_as_read,name='notify-mark-all-as-read'),
    path('notify/delete-all-read/',views.notify_delete_all_read,name='notify-delete-all-read'),
]