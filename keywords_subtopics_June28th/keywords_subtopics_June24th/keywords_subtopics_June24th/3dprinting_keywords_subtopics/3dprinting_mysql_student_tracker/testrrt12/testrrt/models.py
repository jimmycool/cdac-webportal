from optparse import NO_DEFAULT
from django.db import models
from taggit.managers import TaggableManager

class Topic(models.Model):
    id = models.BigAutoField(primary_key=True)
    topic = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.topic

    class Meta:
        db_table = 'Topics'
        managed = True

class SubTopic(models.Model):
    id = models.BigAutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='subtopics')
    subtopic = models.CharField(max_length=100)

    def __str__(self):
        return self.subtopic

    class Meta:
        db_table = 'SubTopics'
        managed = True

class Documents(models.Model):
    name = models.CharField(max_length=100,default=None)
    description = models.TextField()
    #topic=models.ForeignKey(to=Topics,on_delete=models.CASCADE)
    topic=models.TextField(max_length=100)
    subtopics=models.TextField(max_length=100)
    uploaded_at = models.DateTimeField()
    document=models.FileField(upload_to='documents/')
    tags = TaggableManager()
    def __str__(self):
        return self.name
    class Meta:
      db_table ='Documents'
      managed=True

class Video(models.Model):
    id=models.IntegerField(primary_key=True)
    topic=models.TextField(max_length=100,default='default_topic')
    subtopics=models.TextField(max_length=100,default='default_subtopic')
    document=models.FileField(upload_to='videos/')
    description=models.CharField(max_length=100)
    tags = TaggableManager()

    def __str__(self):
        return str(self.document)+self.description
    class Meta:
        db_table='Video'
        managed=True
class DocumentsView(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100,default=None)
    Date=models.DateField()
    Type_doc=models.CharField(max_length=100)
    def __str__(self):
        return str(self.name)+self.Type_doc
    class Meta:
        db_table='DocumentsViewed'
        managed=True
class User1(models.Model):
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(max_length=100)
    '''firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)'''
    password = models.CharField(max_length=100)
    account=models.CharField(max_length=100)
    picture=models.ImageField(upload_to='pic/')
    def __str__(self):
       return self.username
    class Meta:
        db_table = 'User1'
        managed=True
