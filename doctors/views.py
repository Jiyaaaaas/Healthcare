from django.shortcuts import render, redirect
from .models import Doctor, Appointment

def doctor_list(request):
    query = request.GET.get("q")
    spec = request.GET.get("spec")

    doctors = Doctor.objects.all()

    if query:
        doctors = doctors.filter(name__icontains=query)

    if spec:
        doctors = doctors.filter(specialization__icontains=spec)

    return render(request, "doctors.html", {"doctors": doctors})


def book(request, id):
    doctor = Doctor.objects.get(id=id)

    if request.method == "POST":
        Appointment.objects.create(
            user=request.user,
            doctor=doctor,
            date=request.POST["date"],
            problem=request.POST["problem"]
        )
        return redirect("/profile")

    return render(request, "book.html", {"doctor": doctor})