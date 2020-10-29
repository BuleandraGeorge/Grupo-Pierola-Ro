from django.shortcuts import render, redirect


from datetime import date
import datetime
from django.contrib.auth.models import User
from .forms import Age

today = date.today()

def AgeCalc(b_year, b_month, b_day):
    if b_month < today.month:
        age = today.year - b_year - 1
        return age
    else:
        if b_month == today.month:
            if b_day < today.day:
                age = today.year - b_year - 1
                return age
            else:
                age = today.year - b_year
                return age
        else:
            age = today.year - b_year
            return age


def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin')
        else:
            return redirect('home')
    else:
        return redirect('home')


def check_age(request):
    if request.method == "POST":
        form = Age(request.POST)
        date = request.POST['date_of_birth'].split('/')
        day = int(date[0])
        month = int(date[1])
        year = int(date[2])
        age = AgeCalc(year, month, day)
        request.session['age'] = age
        return redirect('home')
    else:
        form = Age()
        context = {
            'form': form
        }
        return render(request, 'user_filter/check_age.html', context)


def under_age(request):
    return render(request, 'user_filter/under_age.html')