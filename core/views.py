from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib import messages
from core.models import Post, Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from django.core.exceptions import ObjectDoesNotExist

@login_required(login_url='signin')
def index(request):
    if request.user.is_authenticated:
        try:
            user_object = User.objects.get(username=request.user.username)
            user_profile = Profile.objects.get(user=user_object)
            posts=Post.objects.all()
            print("User is authenticated")
            return render(request, 'index.html', {'user_profile': user_profile,'posts':posts})
        except ObjectDoesNotExist:
            print("User's profile does not exist")
            return render(request, 'index.html', {"user_profile": None})
    else:
        print("User is not authenticated")
        return render(request, 'signin.html')


def signup(request):
    if request.method == "POST":  # Note the corrected attribute here
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmPassword = request.POST['confirmPassword']
        if(password==confirmPassword):
            if User.objects.filter(email=email).exists():
                 messages.info(request,"Email Already exists")
                 return redirect("signup")
            elif User.objects.filter(username=username).exists():
                 messages.info(request,"username Already exists")
                 return redirect("signup")
            else:
               user = User.objects.create_user(username=username, email=email, password=password)
               user.save()
                #log user in and redirect to settings page
               user_login = auth.authenticate(username=username, password=password)
               auth.login(request, user_login)
                #create a Profile object for the new user
               user_model = User.objects.get(username=username)
               new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
               new_profile.save()
               return redirect('settings')
        else:
            messages.info(request,"password not Matching")
            return redirect("signup")
    else:
        return render(request, 'signup.html')
    
def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user is not None:
            user = auth.authenticate(request, username=user.username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
        
        messages.error(request, 'Invalid credentials')
        return redirect('signin')
    else:
     return render(request, 'signin.html')
    

def logout(request):
    auth.logout(request)
    return redirect('signin')  # Redirect to the 'signin' page after logging out

# @login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')
    return render(request, 'setting.html',{'user_profile': user_profile})

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')