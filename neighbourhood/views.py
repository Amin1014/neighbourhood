from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm, BusinessForm, ProfileForm, ProfileUploadForm, notificationsForm
from .models import Authorities, BlogPost, Business, Health, Profile
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def index(request):
    try:
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')
        current_user=request.user.id
        print(current_user)
        profile =Profile.objects.get(username=current_user)
    except ObjectDoesNotExist:
        # return redirect('create-profile')
        return render(request,'index.html')

@login_required(login_url='/accounts/login/')
def my_profile(request):
    current_user=request.user
    profile =Profile.objects.get(username=current_user)
    return render(request,'profile/user_profile.html',{"profile":profile})

@login_required(login_url='/accounts/login/')
def user_profile(request,username):
    user = User.objects.get(username=username)
    profile =Profile.objects.get(username=user)

@login_required(login_url='/accounts/login/')
def create_profile(request):
    current_user=request.user
    if request.method=="POST":
        form =ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.username = current_user
            profile.save()
        return HttpResponseRedirect('/')
    else:
        form = ProfileForm()
        return render(request,'profile/profile_form.html',{"form":form})

@login_required
def profile(request):
  current_user = request.user
  user_posts = Post.objects.filter(user_id = current_user.id).all()
  return render(request,'profile/profile.html',{'user_posts':user_posts,"current_user":current_user})
@login_required
def update_profile(request):
  if request.method == 'POST':
    user_form = UpdateUser(request.POST,instance=request.user)
    profile_form = UpdateProfile(request.POST,request.FILES,instance=request.user.profile)
    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      messages.success(request,'Your Profile account has been updated successfully')
      return redirect('profile')
  else:
    user_form = UpdateUser(instance=request.user)
    profile_form = UpdateProfile(instance=request.user.profile)
  params = {
    'user_form':user_form,
    'profile_form':profile_form
  }
  return render(request,'profile/update.html',params)

@login_required(login_url='/accounts/login/')
def blog(request):
    current_user=request.user
    profile=Profile.objects.get(username=current_user)
    blogposts = BlogPostForm.objects.filter(neighbourhood=profile.neighbourhood)

    return render(request,'blog/blogs.html',{"blogposts":blogposts})

@login_required(login_url='/accounts/login/')
def view_blog(request,id):
    current_user = request.user

    try:
        comments = Comment.objects.filter(post_id=id)
    except:
        comments =[]

    blog = BlogPost.objects.get(id=id)
    if request.method =='POST':
        form = CommentForm(request.POST,request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.username = current_user
            comment.post = blog
            comment.save()
    else:
        form = CommentForm()

    return render(request,'blog/view_blog.html',{"blog":blog,"form":form,"comments":comments})

@login_required(login_url='/accounts/login/')
def new_blogpost(request):
    current_user=request.user
    profile =Profile.objects.get(username=current_user)

    if request.method=="POST":
        form =BlogPostForm(request.POST,request.FILES)
        if form.is_valid():
            blogpost = form.save(commit = False)
            blogpost.username = current_user
            blogpost.neighbourhood = profile.neighbourhood
            blogpost.profpic = profile.profpic
            blogpost.save()

        return HttpResponseRedirect('/blog')

    else:
        form = BlogPostForm()

    return render(request,'blog/blogpost_form.html',{"form":form})

@login_required(login_url='/accounts/login/')
def businesses(request):
    current_user=request.user
    # profile=Profile.objects.get(username=current_user)
    # businesses = Business.objects.filter(neighbourhood=profile.neighbourhood)

    return render(request,'business/businesses.html',{"businesses":businesses})

@login_required(login_url='/accounts/login/')
def new_business(request):
    current_user=request.user
    profile =Profile.objects.get(username=current_user)

    if request.method=="POST":
        form =BusinessForm(request.POST,request.FILES)
        if form.is_valid():
            business = form.save(commit = False)
            business.owner = current_user
            business.neighbourhood = profile.neighbourhood
            business.save()

        return HttpResponseRedirect('/businesses')

    else:
        form = BusinessForm()

    return render(request,'business/business_form.html',{"form":form})

@login_required(login_url='/accounts/login/')
def health(request):
    current_user=request.user
    profile=Profile.objects.get(username=current_user)
    healthservices = Health.objects.filter(neighbourhood=profile.neighbourhood)

    return render(request,'health/health.html',{"healthservices":healthservices})

@login_required(login_url='/accounts/login/')
def authorities(request):
    current_user=request.user
    profile=Profile.objects.get(username=current_user)
    authorities = Authorities.objects.filter(neighbourhood=profile.neighbourhood)

    return render(request,'authorities/authorities.html',{"authorities":authorities})

@login_required(login_url='/accounts/login/')
def notification(request):
    current_user=request.user
    profile=Profile.objects.get(username=current_user)
    all_notifications = notificationsForm.objects.filter(neighbourhood=profile.neighbourhood)

    return render(request,'notifications/notifications.html',{"notifications":all_notifications})

# # @login_required(login_url='/accounts/login/')
# # def new_notification(request):
# #     current_user=request.user
# #     profile =Profile.objects.get(username=current_user)

# #     if request.method=="POST":
# #         form =notificationsForm(request.POST,request.FILES)
# #         if form.is_valid():
# #             notification = form.save(commit = False)
# #             notification.author = current_user
# #             notification.neighbourhood = profile.neighbourhood
# #             notification.save()

# #             if notification.priority == 'High Priority':
# #                 send_email(profile.name,profile.email,notification.title,notification.notification,notification.author,notification.neighbourhood)

# #         return HttpResponseRedirect('/notifications')


# #     else:
# #         form = notificationsForm()

# #     return render(request,'notifications/notifications_form.html',{"form":form})

@login_required(login_url='/accounts/login/')
def search_results(request):
    current_user = request.user
    # profile =Profile.objects.get(username=current_user)
    if 'business' in request.GET and request.GET["business"]:
        search_term = request.GET.get("business")
        searched_businesses = Business.search_business(search_term)
        message=f"{search_term}"

        print(searched_businesses)

        return render(request,'business/search.html',{"message":message,"businesses":searched_businesses,"profile":profile})

    else:
        message="You haven't searched for any term"
        return render(request,'business/search.html',{"message":message})

# @login_required(login_url='/accounts/login/')
# def article(request,article_id):
#     try:
#         article = Article.objects.get(id = article_id)
#     except DoesNotExist:
#         raise Http404()
#     return render(request,"all-news/article.html", {"article":article})

# @login_required(login_url='/accounts/login/')
# def new_article(request):
#     current_user = request.user
#     if request.method == 'POST':
#         form = NewArticleForm(request.POST, request.FILES)
#         if form.is_valid():
#             article = form.save(commit=False)
#             article.editor = current_user
#             article.save()
#         return redirect('news_of_day')

#     else:
#         form = NewArticleForm()
#     return render(request, 'new_article.html', {"form": form})

@login_required(login_url='/accounts/login/')
def upload_profile(request):
    current_user = request.user 
    title = 'Upload Profile'
    try:
        requested_profile = Profile.objects.get(user_id = current_user.id)
        if request.method == 'POST':
            form = ProfileUploadForm(request.POST,request.FILES)
            if form.is_valid():
                requested_profile.profile_pic = form.cleaned_data['profile_pic']
                requested_profile.bio = form.cleaned_data['bio']
                requested_profile.username = form.cleaned_data['username']
                requested_profile.save_profile()
                return redirect( profile )
        else:
            form = ProfileUploadForm()
    except:
        if request.method == 'POST':
            form = ProfileUploadForm(request.POST,request.FILES)
            if form.is_valid():
                new_profile = Profile(profile_pic = form.cleaned_data['profile_pic'],bio = form.cleaned_data['bio'],username = form.cleaned_data['username'])
                new_profile.save_profile()
                return redirect( profile )
        else:
            form = ProfileUploadForm()

    return render(request,'profile/upload_profile.html',{"title":title,"current_user":current_user,"form":form})

@login_required(login_url='/accounts/login/')
def profile(request):
	 current_user = request.user
	 profile = Profile.objects.all()
	#  follower = Follow.objects.filter(user = profile)

	 return render(request, 'profile/profile.html',{"current_user":current_user,"profile":profile})
