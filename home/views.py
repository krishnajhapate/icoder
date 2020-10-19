from django.shortcuts import render ,HttpResponse ,redirect
from .models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout

# Create your views here.

# Html pages
def home(request):
    allPosts = Post.objects.all()
    context = {'allPosts':allPosts}
    return render(request,'home/home.html',context)

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        contact = Contact(name=name,email=email,phone=phone,content=content)
        if len(name)<3 or len(email)<4 or len(phone)<10 or len(content)<20:
            messages.error(request,"Please fill contact form correctly")
        else:
            contact.save()
            if contact.save:messages.success(request,"Your message has been sent")

    return render(request,'home/contact.html')

def about(request):
    return render(request,'home/about.html')
    
def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query  )
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count()==0 or len(query)==0:
        messages.warning(request,f'No results found for {query}')
    params={'allPosts':allPosts,'query':query}
    return render(request,'home/search.html',params)

# Authentications API
def handleSignup(request):
    if request.method == 'POST':
        # Get all the parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check errorneus input
        # username 
        if len(username)>10:
            messages.error(request,"Username must be under 10 characters !")
            return redirect('home')
        if not username.isalnum():
            messages.error(request,"Username should only contain letters and numbers!")
            return redirect('home')
        if pass1!=pass2:
            messages.error(request,"Your passwords do not match!")
            return redirect('home')

        # Create user
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"Your account has successfully created !")
        return redirect('home')

    else:
        return HttpResponse("404 - not allowed")

def handleLogin(request):
    if request.method == 'POST':
        # Get all the parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username =loginusername, password = loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged In")
            return redirect('home')
        else :
            messages.warning(request,'Invalid login credentials')
            return redirect('home')
    else:
        return HttpResponse("404 - not allowed")
      
def handleLogout(request):
        logout(request)
        messages.success(request,"Successfully Logged Out")
        return redirect('home')
        