from datetime import datetime
import uuid
from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

#note that here i am inherted this models.model in our Profile class
class Profile(models.Model):
    #This line defines a foreign key field called user,
    #which links each profile to a user. It creates a relationship with the user model. When a user is deleted,
    #the on_delete=models.CASCADE option specifies that the associated profile should also be deleted.
    user = models.ForeignKey(User,on_delete=models.CASCADE)  # Example field for the user's name
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images/',default='defult_profile.jpg') 
    location = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user
