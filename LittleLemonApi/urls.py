from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
	path('menu-items/', views.menu_items),
	path('menu-items/<str:id>', views.single_item),
	path('api-token-auth/', obtain_auth_token),
]