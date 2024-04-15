from django.urls import path, include


urlpatterns = [
    path('api/', include('ToDoSource.api.urls'))
]

# Checking git
