from django.contrib import admin
from django.urls import path
from rest_framework import routers
from services import views

urlpatterns = [
    path('admin/', admin.site.urls),
]

router = routers.DefaultRouter()
router.register(r'api/subscriptions', views.SubscriptionView)
urlpatterns += router.urls