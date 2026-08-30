from django import forms
from .models import Documents,Video,User1,Topic,SubTopic
from django.utils import choices
from  django.contrib.auth.models import User,Group
from django.core.exceptions import ValidationError
import re
#print([(topic.topic, topic.topic) for topic in Topic.objects.all()])
#print([(subtopic.subtopic, subtopic.subtopic) for subtopic in SubTopic.objects.all()])
class DocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        tags = kwargs.pop('tags', None)  # safely remove before calling super
        super().__init__(*args, **kwargs)
        self.tags = tags
    
    class Meta:
        model = Documents
        fields = ('name','topic','subtopics','description','uploaded_at','document','tags',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'topic':forms.Select(choices=[(topic.topic, topic.topic) for topic in Topic.objects.all()]),
            'subtopics':forms.Select(choices=[]),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'uploaded_at':forms.DateInput(attrs={'type':'date'}),
            'document': forms.ClearableFileInput(attrs={'class': 'custom-class'}),
            'tags':forms.Textarea(attrs={'class':'form-control','style':'width:200px;height:200px'}) 
        }

class ForgotPassword(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','style':'width:200px;'}))
    class Meta:
        model=User
        fields=('username',)
class ForgotPassword1(forms.ModelForm):
    username=forms.CharField(widget=forms.HiddenInput(),initial=None,disabled=True),
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','style':'width:200px;'}))
    retype=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=('username','password',)
    def clean_title(self):
        pass1 = self.cleaned_data.get('password')
        pass2=self.cleaned_data.get('retype')
        if pass1!=pass2:
            raise ValidationError("The title must be at least 10 characters long.")
            
        return pass1
class SearchDEscription(forms.ModelForm):
    description=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','style':'width:200px;'}))
    class Meta:
        model=Documents
        fields=('description',)
tags1=[('cdac','cdac')]
tags2=[('cdac2','cdac2')]
#tags1=[(tag.name,tag.name) for tag in Documents.tags.all()]
#tags2=[(tag.name,tag.name) for tag in Video.tags.all()]

class SearchForm(forms.ModelForm):
    tags=forms.ChoiceField(choices=tags1,widget=forms.Select(choices=tags1,attrs={'class': 'form-control','style':'width:200px;'}))
    class Meta:
        model=Documents
        fields=('tags',)
        ''' widgets={
            'tags':forms.Select(choices=tags1,attrs={'class': 'form-control'})
        }'''
class Videosearchform(forms.ModelForm):
    tags=forms.ChoiceField(choices=tags1,widget=forms.Select(choices=tags1,attrs={'class': 'form-control','style':'width:200px;'}))
    class Meta:
        model=Video
        fields=('tags',)
        ''' widgets={
            'tags':forms.Select(choices=tags1,attrs={'class': 'form-control'})
        }'''
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('topic','subtopics','document','description','tags')
        widgets = {
            'topic': forms.Select(choices=[(topic.topic, topic.topic) for topic in Topic.objects.all()]),
            'subtopics': forms.Select(choices=[]),
            'description': forms.TextInput(attrs={'class':'form-control'}),
            'document': forms.ClearableFileInput(attrs={'class': 'custom-class'})
        }
class UserForm(forms.ModelForm):
    '''firstname=forms.CharField()
    lastname=forms.CharField()'''
    
    class Meta:
        model = User1
        fields = ('username','email','account','password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
          '''  'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}), '''
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'retypepassword':forms.PasswordInput(attrs={'class':'form-control'}),
            'account':forms.Select(choices=[('Administrator','Administrator'),('Student','student')],attrs={'class':'form-control'})
            }
    firstname=forms.CharField()
    lastname=forms.CharField()
    

    
    
class UpdatePicture(forms.ModelForm):
    picture=forms.ChoiceField(
        choices=[('CR7','cr7'),('Zidane','Zidane'),('Ronaldinho','ronaldinho')],
        widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model=User1
        fields=('username','email','account','picture',)
        

            
class LoginForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('username','password')
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control','style':'width:200px;'}),
            'password':forms.PasswordInput(attrs={'class':'form=control','style':'width:200px;'})
        }
class LoggedIn(forms.ModelForm):
   # Define the field here instead of in Meta widgets
    username = forms.ChoiceField(
        choices=[('cdac1','cdac1'),('cdac2','cdac2'),('cdac50','cdac50')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username',)