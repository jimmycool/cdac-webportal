from django.contrib import admin
from .models import Documents,User1,Video,Topic,SubTopic
@admin.register(User1)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username","email","account"]
@admin.register(Documents)
class DocumentsAdmin(admin.ModelAdmin):
    list_display=["name","topic","description","uploaded_at","document"]
@admin.register(Topic)
class TopicsAdmin(admin.ModelAdmin):
    list_display=["topic"]
@admin.register(SubTopic)
class SubTopicsAdmin(admin.ModelAdmin):
    list_display=["subtopic"]
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display=["document","description"]
      