# from neighbourhood.views import article
from django import forms
from .models import BlogPost, Business, Profile, notifications

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=['username']
class ProfileForm(forms.ModelForm):
	model = Profile
	username = forms.CharField(label='Username',max_length = 30)
	
	bio = forms.CharField(label='Image Caption',max_length=500)
	profile_pic = forms.ImageField(label = 'Image Field')


class ProfileUploadForm(forms.ModelForm):
	class Meta:
		model = Profile
		
		exclude = ['user']

class BlogPostForm(forms.ModelForm):
    class Meta:
        model=BlogPost
        exclude=['username','neighbourhood','profpic']

class BusinessForm(forms.ModelForm):
    class Meta:
        model=Business
        exclude=['owner','neighbourhood']

class notificationsForm(forms.ModelForm):
    class Meta:
        model=notifications
        exclude=['author','neighbourhood','post_date']

# class NewArticleForm(forms.ModelForm):
#     class Meta:
#         model = ''
#         exclude = ['editor', 'pub_date']
#         widgets = {
#             'tags': forms.CheckboxSelectMultiple(),
#         }