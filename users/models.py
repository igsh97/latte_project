from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, password, username):
        
        user = self.model(
            password=password,
            username=username,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username, password=None):
    
        user = self.create_user(
            password=password,
            username=username,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    
    username = models.CharField('아이디', max_length=30, unique=True)
    password = models.CharField('비밀번호', max_length=255)
    profile_img = models.ImageField('프로필 이미지',upload_to="profile_img",blank=True,null=True)
    age = models.IntegerField(blank=True, null=True) # 나이입력
    created_at = models.DateField('가입일', auto_now_add=True)
    updated_at = models.DateField('수정일', auto_now=True)
    is_admin = models.BooleanField('관리자 권한 여부', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password',]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin