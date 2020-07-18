from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator

CERTIFICATE_SOURCE_CHOOSES =  (
        ('Udemy','Udemy'),
        ('Coursera','Coursera'),
        ('Edx','Edx'),
        ('Edureca','Edureca'),
        ('Offline','Offline'),
        ('Intership','Intership'),
        ('Company','Company'),
        ('Other','Other'),
    )

class Skills(models.Model):
    author = models.ForeignKey(to=User, on_delete=CASCADE)
    skill = models.CharField(max_length=150,null=False,blank=False)
    percentage = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)],null=False)

class Hobby(models.Model):
    author = models.ForeignKey(to=User, on_delete=CASCADE)
    hobby = models.CharField(max_length=50,null=False,blank=False)
    about_hobby = models.CharField(max_length=50,null=True,blank=True)

class Education(models.Model):
    author = models.ForeignKey(to=User, on_delete=CASCADE)
    start_year = models.CharField(max_length=4)
    end_year = models.CharField(max_length=4)
    dgree_name = models.CharField(max_length=60)
    about = models.CharField(max_length=200)
    dgree_document = models.FileField(upload_to='dgree_File/')


class Project(models.Model):
    author = models.ForeignKey(to=User, on_delete=CASCADE)
    project_name = models.CharField(max_length=150,null=False,blank=False)
    main_thumbnial = models.ImageField(upload_to='project/',null=False,blank=False)
    contribution = models.CharField(max_length=100)
    about_project = models.TextField(max_length=200,null=True,blank=True)
    cr_date = models.DateTimeField(auto_now_add=True)
    thumbnial_1 = models.ImageField(upload_to='project/',null=True,blank=True)
    thumbnial_2 = models.ImageField(upload_to='project/',null=True,blank=True)
    thumbnial_3 = models.ImageField(upload_to='project/',null=True,blank=True)
    github_project_link = models.CharField(max_length=300,null=True,blank=True)



class Blog(models.Model):
    author = models.ForeignKey(to=User, on_delete=CASCADE)
    text = models.TextField(max_length=200,null=False,blank=False)
    picture = models.ImageField(upload_to='blog/',null=False,blank=False)
    cr_date = models.DateTimeField(auto_now_add=True)
    likes= models.IntegerField(default=0)
    dislikes= models.IntegerField(default=0)

    @property
    def number_of_comments(self):
        return Comment.objects.filter(blog_connected=self).count()



class BlogLike(models.Model):
    blog = models.ForeignKey(Blog, on_delete=CASCADE)
    liked_by = models.ForeignKey(User, on_delete=CASCADE)
    cr_date = models.DateTimeField(auto_now_add=True)

    class Meta:
       unique_together = [['blog', 'liked_by']]


class Certificate(models.Model):
    author = models.ForeignKey(to=User, on_delete=CASCADE)
    certificate_pic = models.ImageField(upload_to='certificate/',null=False, blank=False,default="")
    certificate_title = models.CharField(max_length=100,null=False, blank=False)
    source = models.CharField(max_length=100,choices=CERTIFICATE_SOURCE_CHOOSES,default="Other", null=False, blank=False)
    cr_date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    blog_connected = models.ForeignKey(to=Blog, on_delete=CASCADE)
    author = models.ForeignKey(to=User, on_delete=CASCADE)
    text = models.CharField(max_length=100,null=False,blank=False)
    picture = models.ImageField(upload_to='comment/',null=True,blank=True,default="")
    cr_date = models.DateTimeField(auto_now_add=True)

