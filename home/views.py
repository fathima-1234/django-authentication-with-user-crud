from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages, sessions
from django.contrib.auth.models import User, auth
from django.views.decorators.cache import cache_control 



def admin(request):
    if request.user.is_superuser:
        return redirect('adminpanel')
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)

        if user is not None:
            request.session['username']= username
            login(request,user)
            return redirect('adminpanel')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('admin')
    else:
        return render(request,'admin.html')  

def adminpanel(request):
    if request.user.is_superuser:
        dict_about={
                'users': User.objects.all()
            }
        if 'username' in request.session:
            if  request.method == 'POST':
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                username = request.POST['username']
                email =request.POST['email']
                password = request.POST['password']
                confirm_password = request.POST['confirm_password']

                if first_name.strip()=="" or last_name.strip()=="" or username.strip()=="" or email=="" or password.strip()==" "or confirm_password.strip()=="":
                    messages.info(request, 'fill the required fields ')
                    return redirect(adminpanel)
                elif password==confirm_password:
                    
                    if  User.objects.filter(username=username).exists():
                        messages.info(request, 'username already taken ')
                        return redirect(adminpanel)
                    elif User.objects.filter(email=email).exists():
                        messages.info(request, 'Email is already registered ')
                        return redirect(adminpanel)

                    else:
                        user = User.objects.create_user(username=username,
                        password=password, email=email, first_name=first_name, last_name=last_name)
                        user.set_password(password)
                        user.save()
                        messages.success(request, "The user is created") 
                        return render(request, 'adminpanel.html',dict_about)
                else:
                    messages.info(request, 'Both passwords are not matching')
                    return render(request, 'adminpanel.html',dict_about)
            else:
                print("no post method")
                return render(request, 'adminpanel.html',dict_about)
        else:
            return render(request, 'adminpanel.html',dict_about)
    else:
        return HttpResponse("only admin can access")
 
@cache_control(no_cache=True, must_revalidate =True, no_store=True)
def index(request):
    if 'username' in request.session:
        return render(request, 'index.html')
    else:
        return render(request, 'login.html')




@cache_control(no_cache=True, must_revalidate =True, no_store=True)
def login_user(request):
    if 'username' in request.session:
        return redirect('home')
    if request.method =='POST':
        username = request.POST.get('user')
        password = request.POST.get('pass')
        user = authenticate(username=username,password=password)

        if user is not None:
            request.session['username']= username
            login(request,user)
            return redirect('home')

        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login_user')
            
    else:
        return render(request,'login.html')  

@cache_control(no_cache=True, must_revalidate =True, no_store=True)
def logout_user(request):
    if 'username' in request.session:
        request.session.flush()
        return redirect('login_user')


def signup(request):
    if 'username' in request.session:
        return redirect(login_user)

    if  request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email =request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if first_name.strip()=="" or last_name.strip()=="" or username.strip()=="" or email=="" or password.strip()==" "or confirm_password.strip()=="":
            messages.info(request, 'fill the required fields ')
            return redirect(signup)
        elif password==confirm_password:
            
            if  User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken ')
                return redirect(signup)
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already registered ')
                return redirect(signup)

            else:
                user = User.objects.create_user(username=username,
                password=password, email=email, first_name=first_name, last_name=last_name)
                user.set_password(password)
                user.save()
                print("success")
                return redirect('login_user')
        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect(signup)
    else:
        print("no post method")
        return render(request, 'signup.html')


def edit(request,username):
    dataget = User.objects.get(username = username)
    dataget.delete()
    data = User.objects.all()
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        dataget.first_name = first_name
        dataget.last_name =last_name
        dataget.username = username
        dataget.email = email
        dataget.save()
        
        return redirect('adminpanel')
    return render(request,'adminpanel.html',{'dataget':dataget,'data':data})


def delete(request,username):
    dataget = User.objects.get(username=username)
    dataget.delete()
    messages.success(request, "The user is deleted") 
    return redirect('adminpanel')


def searchuser(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            searched = request.POST['searched']
            user = User.objects.filter(username__icontains = searched)
            context={
            'searched' : searched,
            'user' : user,
            }
            return render(request, 'searchuser.html', context)
        else:
            return render(request, 'searchuser.html')
    else:
        return HttpResponse("only admin can access")