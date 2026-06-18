from django.contrib import admin
from django.urls import path
from core.views import home
from accounts.views import home_view, dashboard_view, login_view, signup_view, logout_view
from doctors.views import doctor_list, book
from predictions.views import predict_heart, predict_diabetes, predict_menstrual, profile_view


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Landing/home page
    path('', home_view, name='home'),

    # Auth
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),

    # Doctors
    path('doctors/', doctor_list, name='doctors'),
    path('book/<int:id>/', book, name='book'),

    # Predictions
    path('predict/heart/', predict_heart, name='predict_heart'),
    path('predict/diabetes/', predict_diabetes, name='predict_diabetes'),
    path('predict/menstrual/', predict_menstrual, name='predict_menstrual'),

    # Side-Bar
    path('profile/', profile_view, name='profile'),
]