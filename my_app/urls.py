from django.urls import path
from .views import business_inquiry, admin_dashboard, approve_inquiry, create_user, decline_inquiry, home, admin_login
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path("", home, name="home"),
    path('inquiry_form/', business_inquiry, name='business_inquiry_api'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('create-user/', create_user, name='create_user'),
    path('approve/<int:inquiry_id>/', approve_inquiry, name='approve_inquiry'),
    path('decline/<int:inquiry_id>/', decline_inquiry, name='decline_inquiry'),
    path('admin-login/', admin_login, name='admin_login'),
    # path('admin-logout/', LogoutView.as_view(next_page='admin_login'), name='admin_logout'),
]
