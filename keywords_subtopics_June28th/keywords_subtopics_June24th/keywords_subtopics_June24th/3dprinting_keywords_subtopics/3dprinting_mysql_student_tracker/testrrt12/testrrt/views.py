from pydoc import doc
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from httpcore import request
from .forms import LoginForm,LoggedIn,DocumentForm, SearchForm,Videosearchform,UserForm,VideoForm,UpdatePicture,ForgotPassword,ForgotPassword1
from  django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
import hashlib
from django.db.models import Q
from .models import Documents,Video,User1,Topic,SubTopic
import json
from django.http import HttpResponse 
import os
user=None            
pic=None
email=None
'''
Upload a Document
'''
class DocumentView(View):
    @method_decorator(login_required)
    def get(self,request):
        return render(request, "Upload.html",{'form':DocumentForm,'picture':pic})
    @method_decorator(login_required)
    def post(self,request):
        if(user.has_perm('testrrt12.add_Documents')):
            form=DocumentForm(request.POST,request.FILES)
            file=request.FILES
            topic=request.GET.get('topic')
            subtopic=request.GET.get('subtopics')
            print(topic,subtopic)
            if form.is_valid():
                # file is saved
                form.save()
            else:
                form = DocumentForm()
            return render(request, "Upload.html", {"form": DocumentForm,'picture':pic})
        else:
            return render(request,"Upload.html",{"form":DocumentForm,'picture':pic})
'''
Upload a Document
'''
from django.contrib.auth.mixins import PermissionRequiredMixin

class DocumentView1(PermissionRequiredMixin,View):
    permission_required = ('testrrt.add_documents')
    raise_exception = True
    @method_decorator(login_required)
    def get(self,request):
        topics = Topic.objects.all()
        subtopic_map = {t.topic: list(set([st.subtopic for st in t.subtopics.all()])) for t in topics}
        return render(request, "upload.html",{'form':DocumentForm,'picture':pic,'subtopic_map': json.dumps(subtopic_map)})
    
    @method_decorator(login_required)
    def post(self,request):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            topic=request.POST.get('topic')
            subtopic=request.POST.get('subtopics')
            if not Topic.objects.filter(topic=topic).exists():
                t=Topic(topic=topic)
                t.save()
            else:
                t=Topic.objects.get(topic=topic)
                t.save()
            st=SubTopic(subtopic=subtopic,topic=t)
            st.save()
            doc = form.save(commit=False)
            idf=Documents.objects.all().last().id  
            doc.id = idf+1
            doc.save()                    
            form.save_m2m()
            topics = Topic.objects.all()
            subtopic_map = {t.topic: [st.subtopic for st in t.subtopics.all()] for t in topics}
            return render(request,"upload.html",{'messages':"File has been uploaded Successfully","form":form,'isAdmin':user.groups.filter(name='Administrator').exists(),'subtopic_map': json.dumps(subtopic_map)})
        else:
            form = DocumentForm()
            messages.error(request,"You donot have permissions to upload the document")
            topics = Topic.objects.all()
            subtopic_map = {t.topic: [st.subtopic for st in t.subtopics.all()] for t in topics}
            return render(request,"upload.html",{'messages':"You donot have permissions to upload the document","form":form,'picture':pic,'isAdmin':user.groups.filter(name='Administrator').exists(),'subtopic_map': json.dumps(subtopic_map)})
'''
Search a Document
'''
class DocumentSearchView(View):
    @method_decorator(login_required)
    def get(self,request):
        global tags1
        tags1=[(tag.name,tag.name) for tag in Documents.tags.all()]
        tags2=[tag.name for tag in Documents.tags.all()]
        # fetch canonical topics and subtopic mapping
        topics_qs = Topic.objects.all()
        topics = [t.topic for t in topics_qs]
        subtopics=list(set([subtopics.subtopic for subtopics in SubTopic.objects.all()]))
        subtopic_map = {t.topic: list(set([st.subtopic for st in t.subtopics.all()])) for t in topics_qs}
        sd=SearchForm()
        sd.fields['tags'].choices = tags1
        tagf=request.GET.get("tags")
        if(tagf==None):
            if(request.GET.get("topics")==None):
                if(request.GET.get("subtopics")==None):
                    return render(request,"search.html",{'form':sd,'picture':pic,'tagsd':tags2,'topics':topics,'subtopics':subtopics,'isAdmin':user.groups.filter(name='Administrator').exists(),'subtopic_map': json.dumps(subtopic_map)})
                else:
                    t=request.GET.get("subtopics")
                    mydata = Documents.objects.filter(subtopics=t)
                    template = loader.get_template('allFiles.html')
                    context = {
                    'files': mydata,
                    'message':message,
                    'isAdmin':user.groups.filter(name='Administrator').exists(),
                    'picture':pic
                    }
                    return HttpResponse(template.render(context, request))
            elif(request.GET.get("subtopics")!=None and request.GET.get("topics")!=None):
                t=request.GET.get("topics")
                st=request.GET.get("subtopics")
                mydata = Documents.objects.filter(topic=t,subtopics=st)
                template = loader.get_template('allFiles.html')
                context = {
                'files': mydata,
                'message':message,
                'isAdmin':user.groups.filter(name='Administrator').exists(),
                'picture':pic
                }
                return HttpResponse(template.render(context, request))
                    
            elif(request.GET.get("topics")!=None):
                t=request.GET.get("topics")
                mydata = Documents.objects.filter(topic=t)
                template = loader.get_template('allFiles.html')
                context = {
                'files': mydata,
                'message':message,
                'isAdmin':user.groups.filter(name='Administrator').exists(),
                'picture':pic
                }
                return HttpResponse(template.render(context, request))
        elif(tagf!=None):
            mydata = Documents.objects.filter(tags__name=tagf)
            template = loader.get_template('allFiles.html')
            context = {
            'files': mydata,
            'message':message,
            'isAdmin':user.groups.filter(name='Administrator').exists(),
            'picture':pic
            }
            return HttpResponse(template.render(context, request))
    @method_decorator(login_required)
    def post(self,request):
        global user
        name=request.POST.get("tags")
        print(name)
        mydata = Documents.objects.filter(tags__name=name)
        template = loader.get_template('allFiles.html')
        context = {
        'files': mydata,
        'message':message,
        'isAdmin':user.groups.filter(name='Administrator').exists(),
        'picture':pic
        }
        return HttpResponse(template.render(context, request))
class DocumentSearchView1(View):
    @method_decorator(login_required)
    def get(self,request,*kwargs):
        global tags1
        print(kwargs['tags'])
        mydata=Documents.objects.all()
        Paginate=Paginator(mydata,2)
        page_number=request.GET.get('page')
        if page_number is None:
            page_number = 1
        tags1=[(tag.name,tag.name) for tag in Documents.tags.all()]
        tags2=[tag.name for tag in Documents.tags.all()]
        sd=SearchForm()
        sd.fields['tags'].choices = tags1
        return render(request,"allfiles.html",{'form':sd,'data1':Paginate.page(page_number),'picture':pic,'tagsd':tags2})

class ForgotPasswordView(View):
    def get(self, request):
        return render(request, "ForgotPassword.html", {'form': LoginForm})
    def post(self, request):
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            # Here you would typically send an email with a password reset link
            messages.success(request, "Password reset instructions have been sent to your email.")
            return redirect("login")
        except User.DoesNotExist:
            messages.error(request, "No user found with this email address.")
            return render(request, "ForgotPassword.html", {'form': LoginForm})
'''
Search Videos
'''
class VideoSearchView(View):
    @method_decorator(login_required)
    def get(self, request):
        tags1 = [(tag.name, tag.name) for tag in Video.tags.all()]
        tags2 = [tag.name for tag in Video.tags.all()]
        sd = Videosearchform()
        sd.fields['tags'].choices = tags1
        tagf = request.GET.get("tags")

        # Build topics and subtopic_map for the template
        topics_qs = Topic.objects.all()
        topics = [t.topic for t in topics_qs]
        subtopics = list(set([s.subtopic for s in SubTopic.objects.all()]))
        subtopic_map = {t.topic: list(set([st.subtopic for st in t.subtopics.all()])) for t in topics_qs}

        # Filtering by tag
        if tagf:
            mydata = Video.objects.filter(tags__name=tagf)
            template = loader.get_template('allFiles1.html')
            context = {
                'files': mydata,
                'message': message,
                'isAdmin': user.groups.filter(name='Administrator').exists(),
                'picture': pic
            }
            return HttpResponse(template.render(context, request))

        # Filtering by topic/subtopic via GET params
        topicf = request.GET.get('topics')
        subf = request.GET.get('subtopics')
        if topicf or subf:
            if topicf and subf:
                mydata = Video.objects.filter(topic=topicf, subtopics=subf)
            elif topicf:
                mydata = Video.objects.filter(topic=topicf)
            else:
                mydata = Video.objects.filter(subtopics=subf)
            template = loader.get_template('allFiles1.html')
            context = {
                'files': mydata,
                'message': message,
                'isAdmin': user.groups.filter(name='Administrator').exists(),
                'picture': pic
            }
            return HttpResponse(template.render(context, request))

        # Default render includes topic/subtopic mapping so the template can show selects
        return render(
            request,
            "search1.html",
            {
                'form': sd,
                'picture': pic,
                'tagsd': tags2,
                'isAdmin': user.groups.filter(name='Administrator').exists(),
                'topics': topics,
                'subtopics': subtopics,
                'subtopic_map': json.dumps(subtopic_map)
            }
        )

    @method_decorator(login_required)
    def post(self, request):
        name = request.POST.get("tags")
        mydata = Video.objects.all()
        if name:
            mydata = Video.objects.filter(tags__name=name)

        paginator = Paginator(mydata, 2)
        page_number = request.GET.get('page')
        if page_number is None:
            page_number = 1
        template = loader.get_template('allFiles1.html')
        context = {
            'files': mydata,
            'message': message,
            'isAdmin': user.groups.filter(name='Administrator').exists(),
            'picture': pic,
            'page_obj': paginator.get_page(page_number)
        }
        return HttpResponse(template.render(context, request))
from django.template import loader
message=None
mydata=None
class DescriptionView(View):
    @method_decorator(login_required)
    def get(self, request,description):
        mydata = Documents.objects.filter(description__icontains=description)
        if(len(mydata)!=0):
            return render(request,'allfiles.html',{'files': mydata,'isAdmin':user.groups.filter(name='Administrator').exists(),'picture':pic})        
        else:
            return redirect('/view')
    @method_decorator(login_required)
    def post(self, request):
        '''mydata = Documents.objects.filter(description=description)
        print(mydata)
        template = loader.get_template('allFiles.html')
        return HttpResponse(template.render({'files': mydata,'isAdmin':user.groups.filter(name='Administrator').exists()}, request))
        '''

class ViewallFiles(View):
    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def get(self,request):
        if(request.method=="GET"):#and (request.user.username=="cdac1" or request.user.username=="cdac2")):
            mydata = Documents.objects.all()
            Paginate=Paginator(mydata,5)
            page_number=request.GET.get('page')
            if page_number is None:
                page_number = 1
            template = loader.get_template('allFiles.html')
            print(user.groups.filter(name='Administrator').exists())
            context = {
                'files': Paginate.page(page_number),
                'message':message,
                'isAdmin':user.groups.filter(name='Administrator').exists(),
                'picture':pic
            }
            return HttpResponse(template.render(context, request))

@login_required(login_url='/login')
@csrf_protect
def download_file(request, id):
    uploaded_file = Documents.objects.get(pk=id)
    response = HttpResponse(uploaded_file.document, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.document.name}"'
    return response
@login_required(login_url='/login')
@csrf_protect
def view_file(request, id):
    uploaded_file = Documents.objects.get(pk=id)
    response = HttpResponse(uploaded_file.document, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{uploaded_file.document.name}"'
    return response
@login_required(login_url='/login')
@csrf_protect
def delete_file(request,id):
    f=Documents.objects.filter(id=id)
    f1=Documents.objects.get(pk=id)
    os.remove("media/"+f1.document.name)
    f.delete()
    message="You deleted a File"
    mydata = Documents.objects.all() 
    template = loader.get_template('allFiles.html')
    context = {
    'files': mydata,
    'isAdmin':user.groups.filter(name='Administrator').exists(),
    }
    return render(request,'allfiles.html',context)
'''
Upload Videos
'''
class VideoView1(PermissionRequiredMixin,View):
    permission_required = ('testrrt.add_video')
    raise_exception = True
    def get(self,request):
        pic=User1.objects.get(username=user).picture
        topics = Topic.objects.all()
        subtopic_map = {t.topic: list(set([st.subtopic for st in t.subtopics.all()])) for t in topics}
        return render(request,'upload1.html',{'form':VideoForm,'picture':pic,'subtopic_map': json.dumps(subtopic_map)})
    def post(self,request):
        form1 = VideoForm(request.POST, request.FILES)
        global pic
        if form1.is_valid():
          # Ensure topic/subtopic records exist and save them on the Video
          topic_val = request.POST.get('topic')
          subtopic_val = request.POST.get('subtopics')
          if topic_val:
              if not Topic.objects.filter(topic=topic_val).exists():
                  t = Topic(topic=topic_val); t.save()
              else:
                  t = Topic.objects.get(topic=topic_val)
              if subtopic_val:
                  if not SubTopic.objects.filter(topic=t, subtopic=subtopic_val).exists():
                      SubTopic(subtopic=subtopic_val, topic=t).save()

          doc = form1.save(commit=False)
          idf=Video.objects.all().last().id  
          doc.id = idf+1
          doc.topic = topic_val
          doc.subtopics = subtopic_val
          pic=User1.objects.get(username=user).picture
          doc.save()                    
          form1.save_m2m()          
          print("Saved")
          messages.success(request,"File has been uploaded Succesfully!!!")
          return render(request,"upload1.html",{'form':form1,'picture':pic})   
        else:
            form1 = VideoForm()
            pic=User1.objects.get(username=user).picture
            return render(request,"upload1.html",{'form':form1,'picture':pic,'isAdmin':user.groups.filter(name='Administrator').exists(),
})
'''
Display all videos
'''        
class VideoView(View):
    @method_decorator(login_required)
    def get(self,request):
        mydata = Video.objects.all()
        paginator=Paginator(mydata,2)
        page_number=request.GET.get('page')
        template = loader.get_template('allFiles1.html')
        context = {
            'files': mydata,
            'message':message,
            'isAdmin':user.groups.filter(name='Administrator').exists(),
            'picture':pic,
            'page_obj':paginator.get_page(page_number)
        }
        return HttpResponse(template.render(context, request))



'''
Selects an Avtaar for the User and also updates the first name,last name
'''
class UpdateProfilePic(View):
    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def get(self,request):
        return render(request,"updateProfilepic.html",{'form':UpdatePicture})
    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def post(self,request):
        global pic
        file=request.POST.get('picture')
        uname1=User1.objects.get(username=user)
        if(file=='CR7'):
            uname1.picture='cristiano-ronaldo-2560x1440-9685.jpg'
        elif(file=='ronaldinho' or file=='Ronaldinho'):
            uname1.picture='ronaldinho.jpg'
        elif(file=='Zidane'):
            uname1.picture='zidane1.jpg'    
        uname1.save()
        #form.save()
        return redirect('home')
        #return render(request,"home.html",{'messages':"Profile Photo has been updated",'form':UpdatePicture,'isadmin':user.groups.filter(name='Administrator').exists(),'picture':uname1.picture})
class LoginView(View):
    def get(self, request):
        messages=None
        return render(request, "login.html",{'form':LoginForm})
    def post(self, request):
        global user,email
        username = request.POST.get("username")
        password = request.POST.get("password")
        m = hashlib.sha256()
        m.update(bytes(password,'utf-8'))
        user = authenticate(request, username=username, password=m.hexdigest())
        if user is not None:
            login(request, user)
            if(user.groups.filter(name='Administrator').exists()):
                pic=User1.objects.get(username=user).picture
                email=User1.objects.get(username=user).email
                mydata = Video.objects.all()[0:3]
                mydata1=Documents.objects.all()[0:3]
                return render(request,'Home.html',{'form':LoginForm,'picture':pic,'email':email,'files':mydata,'files1':mydata1})
            if(user.groups.filter(name='Student').exists()):
                pic=User1.objects.get(username=user).picture
                mydata = Video.objects.all()[0:3]
                mydata1=Documents.objects.all()[0:3]
                return render(request,'Home_student.html',{'form':LoginForm,'picture':pic,'files':mydata,'files1':mydata1})
        else:
            return render(request,"login.html",{'form':LoginForm,'error':"Invalid username or password."})
unames=[]
class HomeView(View):
    @method_decorator(login_required)
    def get(self,request):
        global user,pic       
        if(user.groups.filter(name='Administrator').exists()):
            pic=User1.objects.get(username=user).picture
            mydata = Video.objects.all()[0:3]
            mydata1=Documents.objects.all()[0:3]
            return render(request,"Home.html",{'form':LoginForm,'picture':pic,'files':mydata,'files1':mydata1})
        elif(user.groups.filter(name='student').exists()):
            pic=User1.objects.get(username=user).picture
            mydata = Video.objects.all()[0:3]
            mydata1=Documents.objects.all()[0:3]
            return render(request,'Home_student.html',{'form':LoginForm,'picture':pic,'files':mydata,'files1':mydata1})
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")
unames=[]
import time
from datetime import timedelta
class LastLoggedInTime(View):
    @method_decorator(login_required)
    def get(self, request):
        unames=[]
        global pic
        users=User.objects.values_list()
        for j in range(0,len(users),1): 
            unames.append((users[j][4],users[j][4]))
        tagr = {'username': unames}
        form = LoggedIn()
        # Access the field directly and set the choices
        form.fields['username'].choices = unames
        return render(request, "AllStudents.html",{'form':form,'picture':pic})
    @method_decorator(login_required)
    def post(self,request):
        uname=request.POST.get("username")
        users=User.objects.get(username=uname)
        ty=users.last_login.astimezone
        context={"Time":ty,'picture':pic}
        template = loader.get_template('AllStudents.html')
        return HttpResponse(template.render(context, request))
class RegisterView(View):
    def get(self, request):
        form = UserForm()
        return render(request, "register.html", {"form": form})
    def post(self, request):
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            acc=form.cleaned_data["account"]
            first=form.cleaned_data["firstname"]
            last=form.cleaned_data["lastname"]
            pic=request.FILES
            m = hashlib.sha256()
            m.update(bytes(password,'utf-8'))
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return render(request, "register.html", {"form": form})
            user = User.objects.create_user(username=username,email=email, password=m.hexdigest())
            user.first_name=first
            user.last_name=last
            user.save()
            user1=User1.objects.create(username=username,email=email,password="",account=acc,picture=None)
            user1.save()
            if(acc=='Administrator'):
                group = Group.objects.using('default').get(name='Administrator')
                user.groups.add(group)
                l=LoginForm()
                return render(request,'login.html',{"form":l,"messages": "Registration is successful. Please log in to the Web Portal."})
            elif(acc=='Student'):
                group = Group.objects.using('default').get(name='Student')
                user.groups.add(group)
                l=LoginForm()
                return render(request,'login.html',{"form":l,"messages": "Registration is successful. Please log in to the Web Portal."})
                       
                #return redirect("login")#,{"form":l,"messages": "Registration is successful. Please log in to the Web Portal."})

        else:
            messages.error(request, "Invalid form data.")
            return render(request,"register.html",{"form":UserForm})
import smtplib
from email.mime.text import MIMEText
class ForgotPasswordView(View):
    def get(self,request):
        fgp=ForgotPassword()
        return render(request,'ForgotPassword.html',{"form":fgp})
    def post(self,request):
        SMTP_SERVER = "localhost"
        SMTP_PORT = 8025
        SMTP_USER = ""  
        SMTP_PASS = ""  
        
        print(request.POST.get("username")) 
        # 2. Define Email Attributes
        sender_email = "develop@cdac.in"
        receiver_email = request.POST.get("username")
        uname=User.objects.get(email=receiver_email).username

        body_text = "<html>"+f"<a href='http://127.0.0.1:8000/reset?username={uname}'>Reset Password</a></html>"
        message = MIMEText(body_text, "html", "utf-8")
        message["Subject"] = "Password reset email!!!"
        message["From"] = sender_email
        message["To"] = receiver_email
        try:
        # Connect directly to the local fake SMTP server
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        # Send the raw string conversion of your MIME object
                server.sendmail(sender_email, receiver_email, message.as_string())
                print("🚀 Please reset your password!")
              
        except ConnectionRefusedError:
            print(f"❌ An error occured while connecting to Fake SMTP server: ")
        except Exception as e:
            print(f"❌ An error occured which prevented the Fake SMTP server working: {e}")
        
        return redirect("login")
class ResetPasswordView(View):
    def get(self,request):
        fg=ForgotPassword1()
        fg.username=request.GET.get("username")
        return render(request,"resetPassword.html",{"form":fg})
    def post(self,request):
        uname1=request.GET.get("username")
        user1=User.objects.get(username=uname1)
        pass1=request.POST.get("password")
        m = hashlib.sha256()
        m.update(bytes(pass1,'utf-8'))
        user1.set_password(m.hexdigest())
        user1.save()
        user2=User1.objects.get(username=uname1)
        user2.password=m.hexdigest()
        user2.save()
        return redirect("login")
