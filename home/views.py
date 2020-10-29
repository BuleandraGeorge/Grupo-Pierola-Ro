from django.shortcuts import render, redirect

# Create your views here.


def home(request):
    age = request.session.get('age', 0)
    if (age != 0) & (age > 17):
        return render(request, "home/home.html")
    else:
        if age == 0:
            return redirect('checkage')
        else:
            return redirect('underage')
