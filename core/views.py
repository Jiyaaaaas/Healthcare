from django.shortcuts import render
from doctors.models import Appointment



def home(request):
    return render(request, "home.html")


def profile(request):
    data = Appointment.objects.filter(user=request.user)
    return render(request, "profile.html", {"data": data})