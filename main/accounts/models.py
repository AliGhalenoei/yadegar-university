from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin



class User(PermissionsMixin , AbstractBaseUser):
    email = models.EmailField(max_length=60 , unique=True , verbose_name="ایمیل کاربر")
    username = models.CharField(max_length=255 , verbose_name="نام کاربری")
    password = models.CharField(max_length=255 , verbose_name="رمزعبور")

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj = None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    

class OTP(models.Model):
    email = models.EmailField()
    code = models.SmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} Code Verify : {self.code}"
    
    def save(self, *args , **kwargs):
        exist_otp = OTP.objects.filter(email = self.email)
        if exist_otp.exists():
            exist_otp.delete()
        return super().save( *args , **kwargs)


