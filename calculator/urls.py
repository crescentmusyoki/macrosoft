from django.urls import path

from calculator.views import LoginView, RegisterView, logout_view, HomeView, ProfileView, change_password, HistoryView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login-view'),
    path('register/', RegisterView.as_view(), name='register-view'),
    path('logout/', logout_view, name='logout-view'),
    path('profile/', ProfileView.as_view(), name='profile-view'),
    path('change-password/', change_password, name='change-password-view'),
    path('history/', HistoryView.as_view(), name='history-view'),
    path('', HomeView.as_view(), name='home-view'),
]
