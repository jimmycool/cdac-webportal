"""
URL configuration for testrrt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for site1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings
from .views import LoginView,ForgotPasswordView,ResetPasswordView,DescriptionView,ViewallFiles,DocumentSearchView1,LastLoggedInTime,VideoView1,RegisterView,UpdateProfilePic,view_file,LogoutView,VideoView,DocumentSearchView,VideoSearchView,VideoView1,HomeView,DocumentView,DocumentView1,VideoView,download_file,delete_file
admin.site.site_header = "3d printing LMS"      
admin.site.site_title = "3d Printing LMS"             
admin.site.index_title = "Welcome to the 3d printing portal(LMS)"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('register/', RegisterView.as_view(), name='register'),
    path('search/', DocumentSearchView.as_view(), name='search'),
    path('search1/<int:page>',DocumentSearchView1.as_view(),name='search2'),
    path('all/',LastLoggedInTime.as_view(),name='users_Logged_in'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/',HomeView.as_view(),name='home'),
    path('upload/',DocumentView1.as_view(),name='upload'),
    path('description/<str:description>/',DescriptionView.as_view(),name='description'),
    path('view/',ViewallFiles.as_view(),name='view'),
    path('Picture/',UpdateProfilePic.as_view(),name="Profile pic update"),
    path('reset/',ResetPasswordView.as_view(),name="reset password"),
   # path('rest/',ForgotPasswordView.as_view(),name='forgot password'),
    path('view1/',VideoView.as_view(),name='videos'),
    #path('search1/<int:page>',VideoView2.as_view(),name="Search All"),
    path('download/<int:id>',download_file),
    path('viewfile/<int:id>',view_file),
    path('paginate/<int:limit>/<int:start>',view_file),
    path('delete/<int:id>',delete_file),
    path('upload_video/',VideoView.as_view(),name="View Videos"),
    path('upload_video1/',VideoView1.as_view(),name="Upload Videos"),
    path('search_video/',VideoSearchView.as_view(),name='Search Videos')
    ]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
