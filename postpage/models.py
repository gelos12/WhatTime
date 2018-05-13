from django.db import models
from authpage.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField('제목',max_length=120)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    password = models.CharField('비밀번호',max_length=120)
    use_user = models.ManyToManyField(User,blank=True,verbose_name='user_User_related',
        related_name='use_user_related',through='use')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
    @property
    def use_user_count(self):
        return self.use_user_related.count()

    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.pk})

class Use(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
