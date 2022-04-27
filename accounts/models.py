
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
import random
from django.core.validators import RegexValidator

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password,**other_fields):
        if not email:
            raise ValueError('The Email is mandatory')
        if not username:
            raise ValueError('The username is mandatory')

        user = self.model(
            email= self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,**other_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,first_name,last_name,username,email,password,**other_fields):

        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)
        other_fields.setdefault('is_admin',True)
        
    #  this is and validation checkup while creation method
        if other_fields.get('is_staff') is not True:
            raise ValueError('Super user is_staff must be True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser must set to True')
        if other_fields.get('is_active') is not True:
            raise ValueError('is_active must be set to True')
        if other_fields.get('is_admin') is not True:
            raise ValueError('is_admin must be set to True')

        return self.create_user(first_name,last_name,username,email,password,**other_fields)
    

class Account(AbstractBaseUser,PermissionsMixin):
    ''' This is the user models which created the help of abstract Base User , we need to 
    write every things from the scratch in this AbstractBaseUser '''

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    phone = models.CharField(max_length=20)

    # extra added tta 
    #required 
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    def __str__(self):
        return self.email


class UserProfile(models.Model):

    
    user = models.OneToOneField(Account,on_delete=models.CASCADE,related_name='profile')
    profile_pic = models.ImageField(upload_to='profile/',max_length=500,default='profile/avatar.png')
    # 
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    username = models.CharField(max_length=100,null=True)
    email = models.EmailField(max_length=100,null=True)
    phone = models.CharField(max_length=15, validators=[RegexValidator(r'^\d{1,15}$')])
    address_line_1 = models.TextField(max_length=300,null=True)
    address_line_2 = models.TextField(max_length=300,null=True)
    country = models.CharField(max_length=50,null=True)
    state = models.CharField(max_length=50,null=True)
    city = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.user.username

class UserAddress(models.Model):
    STATUS = (
        ('HOME', 'HOME'),
        ('OFFICE', 'OFFICE'),
        ('OTHERS', 'OTHERS'),
    )
    
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15, validators=[RegexValidator(r'^\d{1,15}$')])
    address_line_1 = models.TextField(max_length=300)
    address_line_2 = models.TextField(max_length=300)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=STATUS, default='HOME')

    def __str__(self):
        return self.first_name+' '+ self.last_name
    