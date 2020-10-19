from django.shortcuts import render ,redirect
from django.http import HttpResponse 
from blog.models import Post ,BlogComment
from django.contrib import messages
from blog.templatetags import extras
# Create your views here.


def blogHome(request):
    allPosts = Post.objects.all()
    context={'allPosts':allPosts}
    return render(request,'blog/bloghome.html',context)

def blogPost(request,slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post,parent=None) 
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    try:
        for reply in replies:
            if reply.parent.sno not in replyDict.keys():
                replyDict[reply.parent.sno]=[reply]
            else:
                replyDict[reply.parent.sno].append(reply)
    except:pass
    context = {'post':post,'comments':comments,'user':request.user,'replyDict':replyDict}
    return render(request,'blog/blogPost.html',context)

def postComment(request):
    if request.method=="POST":
        comment = request.POST['comment']
        user = request.user
        postSno = request.POST["postSno"]
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST["parentSno"]
        if parentSno=="":
            comment = BlogComment(user=user,post=post,comment=comment)
            comment.save()
            messages.success(request,f'{request.user} commented')
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(user=user,post=post,comment=comment,parent=parent)
            comment.save()
            messages.success(request,f'{request.user} replyed to {parent.user}"s" comment')
        
        return redirect(f'/blog/{post.slug}')
    
    return redirect('/')

def commentdelete(request):
    if request.method == "POST":
        commentdel = request.POST.get('delcomment')
        delpostcommentsno = request.POST.get('delpostcommentsno')
        delcomm= BlogComment.objects.get(sno=commentdel).delete()
        post = Post.objects.filter(sno=delpostcommentsno)
        print(delcomm)
        # delcomm.delete()
        messages.success(request,"Your comment has been deleted")
        return redirect(f'/blog/{post.slug}')     
    else: 
        return HttpResponse("404 not found")     

    