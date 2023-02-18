from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django_mysql.models import ListTextField



class User(AbstractUser):
    ROLE_CHOICES = [
        ['tester', 'Tester'],
        ['developer', 'Developer'],
        ['project_manager', 'Project Manager']
    ]


    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=90, unique=True)
    is_organizer = models.BooleanField(default=True)
    is_member = models.BooleanField(default=False)
    role = models.TextField(choices=ROLE_CHOICES)
    ticket_flow = models.ManyToManyField('Project', blank=True)
    email_confirmed = models.BooleanField(default=False)

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Project(models.Model):
    PROGRESS_CHOICES = [
        ('opened', 'Opened'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=1000, blank=True, null=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    progress = models.TextField(choices=PROGRESS_CHOICES, null=True)
    organisation = models.ForeignKey(Account, on_delete=models.CASCADE, blank=False, null=False)
    project_manager = models.ForeignKey("Member", null=True, blank=True, on_delete=models.SET_NULL)
    color_code = models.CharField(max_length=100, default='#563d7c')
    archive = models.BooleanField(default=False)
    total_score = ListTextField(base_field=models.PositiveIntegerField(), size=None, default=0)

    def append_total_score(self):
        value = self.total_score[-1]
        self.total_score.append(value)
        self.save()

    def subtract_total_score(self, value):
        value = self.total_score.pop() - value
        self.total_score.append(value)
        self.save()

    def add_total_score(self, value):
        value = self.total_score.pop() + value
        self.total_score.append(value)
        self.save()

    def __str__(self):
        return self.title



class Status(models.Model):
    name = models.CharField(max_length=30)
    organisation = models.ForeignKey(Account, on_delete=models.CASCADE)
    color_code = models.CharField(max_length=100, default='#563d7c')
    test_status = models.BooleanField(default=False)

    def __str__(self):
        if self.name:
            return self.name


class Priority(models.Model):
    name = models.CharField(max_length=30)
    organisation = models.ForeignKey(Account, on_delete=models.CASCADE)
    color_code = models.CharField(max_length=100, default='#563d7c')

    def __str__(self):
        if self.name:
            return self.name

class Type(models.Model):
    name = models.CharField(max_length=30)
    organisation = models.ForeignKey(Account, on_delete=models.CASCADE)
    color_code = models.CharField(max_length=100, default='#563d7c')

    def __str__(self):
        if self.name:
            return self.name


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Ticket(models.Model):
    title = models.CharField(max_length=32)
    organisation = models.ForeignKey(Account, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey("Member", null=True, blank=True, on_delete=models.SET_NULL)
    status = models.ForeignKey("Status", null=True, blank=True, on_delete=models.SET_NULL)
    priority = models.ForeignKey("Priority", null=True, blank=True, on_delete=models.SET_NULL)
    type = models.ForeignKey("Type", null=True, blank=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(default=timezone.now)
    deadline = models.DateField(blank=False, null=True)
    description = models.TextField(max_length=1000, blank=False, null=False)
    author = models.ForeignKey("User", null=True, blank=True, on_delete=models.SET_NULL, related_name='tickets')
    project = models.ForeignKey('Project', related_name='tickets', on_delete=models.CASCADE)
    tester = models.ForeignKey("User", null=True, blank=True, on_delete=models.SET_NULL)
    score = IntegerRangeField(min_value=0, max_value=50, null=True, blank=True, default=0)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


def handle_upload_comments(instance, filename):
    return f"ticket_comments/ticket_{instance.ticket.pk}/{filename}"

class Notification(models.Model):
    title = models.TextField()
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    recipient = models.ForeignKey('User', on_delete=models.CASCADE, related_name='notifications')


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey("User", null=True, blank=True, on_delete=models.SET_NULL)
    date_added = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=False, null=True)
    file = models.FileField(null=True, blank=True, upload_to=handle_upload_comments)

    def __str__(self):
        return self.ticket.title


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)