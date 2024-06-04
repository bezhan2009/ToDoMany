from django.urls import path

from .views import UserView, UserProfileDetails

urlpatterns = [
    path('sign-up/', UserView.as_view(), name='sign_up'),
    path('details/', UserProfileDetails.as_view(), name='detail'),
]
