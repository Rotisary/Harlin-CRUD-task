from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("users must have an email address")
        if not username:
            raise ValueError("users must have a username")
        

        user = self.model(
            email = self.normalize_email(email),
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
        

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password
        )
        
        user.is_verified = True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, 
                              verbose_name='email', 
                              unique=True, 
                              null=False, 
                              blank=False)
    username = models.CharField(max_length=30, 
                                unique=True, 
                                null=False, 
                                blank=False)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True, null=False)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True, null=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verif_code = models.IntegerField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()


    def __str__(self):
        return f"{self.username}"
    

    def has_perm(self, perm, obj=None):
        return self.is_admin
    

    def has_module_perms(self, app_label):
        return True
