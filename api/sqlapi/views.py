from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Create your views here.
import pickle
import keras
import tensorflow as tf
from tensorflow import keras

mymodel = tf.keras.models.load_model('sqlidetector.h5')
myvectorizer = pickle.load(open("vectorizer_additional_data", 'rb'))

def clean_data(input_val):
    input_val = input_val.replace('\n', '')
    input_val = input_val.replace('%20', ' ')
    input_val = input_val.replace('=', ' = ')
    input_val = input_val.replace('((', ' (( ')
    input_val = input_val.replace('))', ' )) ')
    input_val = input_val.replace('(', ' ( ')
    input_val = input_val.replace(')', ' ) ')
    input_val = input_val.replace('1 ', 'numeric')
    input_val = input_val.replace(' 1', 'numeric')
    input_val = input_val.replace("'1 ", "'numeric ")
    input_val = input_val.replace(" 1'", " numeric'")
    input_val = input_val.replace('1,', 'numeric,')
    input_val = input_val.replace(" 2 ", " numeric ")
    input_val = input_val.replace(' 3 ', ' numeric ')
    input_val = input_val.replace(' 3--', ' numeric--')
    input_val = input_val.replace(" 4 ", ' numeric ')
    input_val = input_val.replace(" 5 ", ' numeric ')
    input_val = input_val.replace(' 6 ', ' numeric ')
    input_val = input_val.replace(" 7 ", ' numeric ')
    input_val = input_val.replace(" 8 ", ' numeric ')
    input_val = input_val.replace('1234', ' numeric ')
    input_val = input_val.replace("22", ' numeric ')
    input_val = input_val.replace(" 8 ", ' numeric ')
    input_val = input_val.replace(" 200 ", ' numeric ')
    input_val = input_val.replace("23 ", ' numeric ')
    input_val = input_val.replace('"1', '"numeric')
    input_val = input_val.replace('1"', '"numeric')
    input_val = input_val.replace("7659", 'numeric')
    input_val = input_val.replace(" 37 ", ' numeric ')
    input_val = input_val.replace(" 45 ", ' numeric ')
    return input_val


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('register')  # Add a login page later
    else:
        return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboar')  # create dashboard later
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')

def user_input_view(request):
    result = None  # Default result
    val = None
    if request.method == 'POST':
        name = request.POST.get('name')
        val = name
        # Clean the input
        cleaned_input = clean_data(name)
        cleaned_input = [cleaned_input]  # model expects list

        # Vectorize the input
        input_val = myvectorizer.transform(cleaned_input).toarray()

        # Predict
        prediction = mymodel.predict(input_val)

        # Interpret prediction
        if prediction > 0.5:
            result = "⚠️ ALERT: Possible SQL Injection detected!"
        else:
            result = "✅ Safe input."

    return render(request, 'input.html', {'result': result,'val':val,})



