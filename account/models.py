from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
# models -  MyAccountManager , Account

class MyAccountManager(BaseUserManager):

    def create_user(self, email, userID, username, password= None):
        if not email:
            raise ValueError("User must have an Email Address")
        if not username:
            raise ValueError("User must have a Name")
        if not userID:
            raise ValueError("User must have an Idenficatin Number(ID)")
        user = self.model(
            email = self.normalize_email(email),
            userID =userID,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, userID, password, username):
        user = self.create_user(
            email = self.normalize_email(email),
            userID = userID,
            password = password,
            username = username,
        )
        user.is_superuser = True
        user.is_doctor = True
        user.save(using=self._db)
        return user



def userphoto_path(self, filename):
    name, ext = filename.split(".")
    name = self.userID
    filename = name +'.'+ ext
    return f'user_photos/{filename}'

def defaultphoto_path():
    return 'default_photo/default_userprofile_pic.png'

class Account(AbstractBaseUser):
    GENDER = (
        ('Male','Male'),
        ('Female','Female'),
    )

    BLOOD_GROUP = (
        ("A+ve", "A+"),
        ("A-ve", "A-"),
        ("B+ve", "B+"),
        ("B-ve", "B-"),
        ("O+ve", "O+"),
        ("O-ve", "O-"),
        ("AB+ve", "AB+"),
        ("AB-ve", "AB-"),
    )

    email = models.EmailField(verbose_name = 'Email' , unique=True , max_length=100)
    userID = models.CharField(max_length=8, unique=True, primary_key = True)

    username = models.CharField(max_length=100, verbose_name = 'Full Name')
    date_joined = models.DateTimeField(verbose_name="Date Joined" , auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last Login" , auto_now=True)

    is_active = models.BooleanField(default=True)
    is_doctor = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    father_name = models.CharField(max_length=50, null = True, blank = True)
    age = models.IntegerField(null = True, blank = True)
    gender = models.CharField(max_length=10 , choices=GENDER, null = True, blank = True)
    blood_group = models.CharField(max_length=10 , choices=BLOOD_GROUP, null = True, blank = True)
    number = models.CharField(max_length=10, null = True, blank = True)
    emergency_number = models.CharField(max_length=10, null = True, blank = True)
    userphoto = models.ImageField(upload_to = userphoto_path , default = defaultphoto_path, verbose_name= "Photo" ,null = True, blank = True, max_length=255)


    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['userID', 'username']

    def __str__(self):
        return self.userID

    def has_perms(self,perm, obj=None):
        for per in perm:
            if 'is_doctor' == per:
                return self.is_doctor
            elif 'is_superuser' == per:
                return self.is_superuser

    def has_perm(self, perm , obj= None):
        return self.is_superuser

    def has_module_perms(self , app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def is_admin(self):
        return self.is_superuser
