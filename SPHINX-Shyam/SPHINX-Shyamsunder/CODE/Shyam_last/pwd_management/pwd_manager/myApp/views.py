from cryptography.fernet import InvalidToken
from django.contrib.auth.models import User
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
import random
from django.core.mail import send_mail
from cryptography.fernet import Fernet
from mechanize import Browser
import favicon
from .models import Password
import secrets
import string
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

def encrypt(key, plaintext):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()

    # Ensure the plaintext is padded to a multiple of the block size
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()

    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return ciphertext

def decrypt(key, ciphertext):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()

    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad the plaintext to get the original message
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext

def generate_random_key(length):
    characters = string.ascii_letters + string.digits
    random_key = ''.join(secrets.choice(characters) for _ in range(length))
    # Ensure the key size is at least 16 bytes (128 bits)
    while len(random_key.encode('utf-8')) < 16:
        random_key += secrets.choice(characters)
    return random_key.encode('utf-8')

br = Browser()
br.set_handle_robots(False)


def myView(request):
    if request.method == "POST":
        if "signup-form" in request.POST:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")
            #if password are not identical
            if password != password2:
                msg = "Please make sure you're using the same password!"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            #if username exists
            elif User.objects.filter(username=username).exists():
                msg = f"{username} already exists!"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            #if email exists
            elif User.objects.filter(email=email).exists():
                msg = f"{email} already exists!"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            else:
                User.objects.create_user(username, email, password)
                new_user = authenticate(request, username=username, password=password2)
                if new_user is not None:
                    login(request, new_user)
                    msg = f"{username}. Thanks for subscribing."
                    messages.success(request, msg)
                    return HttpResponseRedirect(request.path)
        elif "logout" in request.POST:
            msg = f"{request.user}. You logged out."
            logout(request)
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)

        elif 'login-form' in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            new_login = authenticate(request, username=username, password=password)
            if new_login is None:
                msg = f"Login failed! Make sure you're using the right account."
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            else:
                code = str(random.randint(100000, 999999))
                global global_code
                global_code = code
                send_mail(
                    "Django Password Manager: confirm email",
                    f"Your verification code is {code}.",
                    settings.EMAIL_HOST_USER,
                    [new_login.email],
                    fail_silently=False,
                )
                return render(request, "home.html", {
                    "code":code, 
                    "user":new_login,
                })


        elif "sentil" in request.POST:
            return render(request, "home.html", {
                "activator": True,
                "user": request.user,
                "url":request.session.get('url',None)
            })

        elif "confirm" in request.POST:
            input_code = request.POST.get("code")
            user = request.POST.get("user")
            if input_code != global_code:
                msg = f"{input_code} is wrong!"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            else:
                login(request, User.objects.get(username=user))
                msg = f"{request.user} welcome again."
                messages.success(request, msg)
                return HttpResponseRedirect(request.path)
        
        elif "add-password" in request.POST:
            url = request.POST.get("url")
            email = request.POST.get("email")
            password = request.POST.get("password")
            #adding details to session
            request.session["url"]=url
            request.session["email"]=email
            
            #get title of the website
            try:
                br.open(url)
                title = br.title()
            except:
                title = url
            #get the logo's URL
            try:
                icon = favicon.get(url)[0].url
            except:
                icon = "https://cdn-icons-png.flaticon.com/128/1006/1006771.png"
            rod = generate_random_key(16)
            rode=rod.decode('utf-8')
            ropas=password.encode('utf-8')
            epass=encrypt(rod,ropas)
            # dpass=decrypt(rod,epass)
            node=base64.b64encode(epass).decode('utf-8')
            print(epass,"epass",len(epass))
            print(node,"rode",len(node))
            send_mail(
                    "Django Password Manager: get Details {url}",
                    f"Your reveal code is {rode}.",
                    settings.EMAIL_HOST_USER,
                    [request.user.email],
                    fail_silently=False,
                )
            #Save data in database
            new_password = Password.objects.create(
                user=request.user,
                name=title,
                logo=icon,
                email=email,
                password=node,
            )
            msg = f"{title} added successfully."
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)
        elif "organo" in request.POST:
            code = request.POST.get("mode")
            url = request.session.get('url', None)
            email = request.session.get('email', None)
            password = request.POST.get('passw', None)
            b=password
            a=code.encode('utf-8')
            ropas=base64.b64decode(b)
            print(len(ropas),"is",ropas,"hero",len(b),"is",b,"hero",len(a),"is",a,"hero")
            dpass=decrypt(a,ropas)
            dpass=dpass.decode('utf-8')
            return render(request, "home.html", {
                "loha": True,
                "url": url,
                "email": email,
                "password": dpass,
            })
        elif "delete" in request.POST:
            to_delete = request.POST.get("password-id")
            msg = f"{Password.objects.get(id=to_delete).name} deleted."
            Password.objects.get(id=to_delete).delete()
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)
            
    context = {}
    if request.user.is_authenticated:
        passwords = Password.objects.all().filter(user=request.user)
        for password in passwords:
            password.email = password.email
            password.password =password.password
        context = {
            "passwords":passwords,
        }   



    return render(request, "home.html", context)