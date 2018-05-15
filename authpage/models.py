from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser  
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail  
from django.contrib.auth.models import PermissionsMixin  
from django.contrib.auth.base_user import AbstractBaseUser  
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.validators import validate_email
from django.utils.crypto import salted_hmac

class UserManager(BaseUserManager):  
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):  
    email = models.EmailField(_('email address'), unique=True, validators=[validate_email])
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.password).hexdigest()

    def __str__(self):
        return str(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('authpage:setting', kwargs={'pk': self.pk})

class SCHEDULE(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE,verbose_name="related user", related_name="schedule")
    time = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email