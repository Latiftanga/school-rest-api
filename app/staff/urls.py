from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

from staff import views


router = DefaultRouter()
router.register(r'', views.StaffViewSets, basename='staff')


app_name = 'staff'


urlpatterns = [
    path('/', include(router.urls)),
]
