from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .constants import USER_TYPE_CHOICES  # Assuming you have this defined elsewhere

class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    date_joined = models.DateTimeField(default=timezone.now)
    email = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    username = None  # Disable username field
    password = models.CharField(max_length=50)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=3)
    is_deleted = models.BooleanField(default=False)
    rfid = models.CharField(max_length=100,  blank=True, null=True)
    CNE = models.CharField(max_length=50,  blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Session(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    prof_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sessions_as_professor', default=None)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    module_id = models.ForeignKey('Module', on_delete=models.CASCADE, related_name='sessions', blank=True, null=True)
    titre = models.CharField(max_length=100)
    discreption = models.CharField(max_length=400)
    is_deleted = models.BooleanField(default=False)

class Module(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=50, unique=True)
    prof_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='modules_as_professor', default=None)
    is_deleted = models.BooleanField(default=False)

class Inscrire(models.Model):
    student_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='inscriptions', default=None)
    module_id = models.ForeignKey('Module', on_delete=models.CASCADE, related_name='inscriptions_module', blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

class Presence(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    student_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='presences', default=None)
    session_id = models.ForeignKey('Session', on_delete=models.CASCADE, related_name='presences_session', blank=True, null=True)
    pointing = models.TimeField()
    is_deleted = models.BooleanField(default=False)

