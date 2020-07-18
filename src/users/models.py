from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from PIL import Image


class Profile(models.Model):

    GENDER_CHOICES = (
        ('male','male'),
        ('female','female'),
        ('other','other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False, blank=False,default="")
    image = models.ImageField(upload_to='image',default='default.png', null=True, blank=True)
    field = models.CharField(max_length=100,null=True,blank=True)
    age = models.IntegerField(null=True, blank=True)
    phone_no = models.CharField(validators=[RegexValidator("^0?[5-9]{1}\d{9}$")], max_length=51, null=True, blank=True)
    location = models.CharField(max_length=200,null=True)
    about = models.CharField(max_length=300,null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=50,null=True,blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    

    @property
    def followers(self):
        return Follow.objects.filter(follow_user=self.user).count()

    @property
    def following(self):
        return Follow.objects.filter(user=self.user).count()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follow_user = models.ForeignKey(User, related_name='follow_user', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)



