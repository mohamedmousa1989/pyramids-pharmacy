from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import (
    RegisterView,
    LoginView,
    MedicationAPIView,
    RefillRequestAPIView,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('medications/', MedicationAPIView.as_view(), name='medications'),
    path('refill-requests/', RefillRequestAPIView.as_view(), name='refill_requests'),
]