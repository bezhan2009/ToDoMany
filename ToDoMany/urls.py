"""
URL configuration for ToDoMany project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView
)

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourdomain.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        print("He")
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            print("Token generated successfully:", response.data)
        else:
            print("Token generation failed:", response.data)
        return response


urlpatterns = [
    path('admin/', admin.site.urls),  # Оставьте только одно определение для 'admin/'
    path('auth/', include('userapp.urls'), name='sign_up'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='verify_refresh'),
    path('auth/sign-in/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('api/tasks/', include('taskapp.urls')),
    path('api/environment/', include('envapp.urls')),
    path('api/comment/', include('commentapp.urls')),
    path('api/team/', include('teamapp.urls')),
    path('api/application/', include('app.urls')),
    path('api/admin/', include('adminapp.urls')),
]
