from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

class TicketCreateModelForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = (
            'title',
            'assigned_to',
            'project',
            'deadline',
            'description',
            'status',
            'priority',
            'type',
            'score'
        )
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        user = request.user
        developer_id = User.objects.filter(role='developer').values_list('id')
        archived = False
        if user.is_organizer:
            members = Member.objects.filter(user_id__in=developer_id, organisation=user.account)
            projects = Project.objects.filter(organisation=user.account, archive=archived)
            statuses = Status.objects.filter(organisation=user.account)
            priorities = Priority.objects.filter(organisation=user.account)
            types = Type.objects.filter(organisation=user.account)
        elif user.role == 'tester':
            statuses = Status.objects.filter(organisation=user.member.organisation)
            priorities = Priority.objects.filter(organisation=user.member.organisation)
            types = Type.objects.filter(organisation=user.member.organisation)
            results = User.objects.filter(id=user.id)
            for usr in results:
                proj = list(usr.ticket_flow.all())
            projects = Project.objects.filter(title__in=proj, organisation=user.member.organisation)
            user_id = User.objects.filter(ticket_flow__in=projects, role='developer').values_list('id', flat=True)
            members = Member.objects.filter(user_id__in=user_id, organisation=user.member.organisation)
        else:
            statuses = Status.objects.filter(organisation=user.member.organisation)
            priorities = Priority.objects.filter(organisation=user.member.organisation)
            types = Type.objects.filter(organisation=user.member.organisation)
            members = Member.objects.filter(user=user, organisation=user.member.organisation)
            results = User.objects.filter(id=user.id)
            for usr in results:
                proj = list(usr.ticket_flow.all())
            projects = Project.objects.filter(title__in=proj, organisation=user.member.organisation)
        super(TicketCreateModelForm, self).__init__(*args, **kwargs)
        self.fields["status"].queryset = statuses
        self.fields["priority"].queryset = priorities
        self.fields["type"].queryset = types
        self.fields["deadline"] = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.now().date()}))
        self.fields["assigned_to"].queryset = members
        self.fields["project"].queryset = projects

class TicketUpdateModelForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = (
            'title',
            'assigned_to',
            'project',
            'deadline',
            'description',
            'status',
            'score'
        )
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        user = request.user
        developer_id = User.objects.filter(role='developer').values_list('id')
        archived = False
        super(TicketUpdateModelForm, self).__init__(*args, **kwargs)
        if user.is_organizer:
            members = Member.objects.filter(user_id__in=developer_id, organisation=user.account)
            projects = Project.objects.filter(organisation=user.account, archive=archived)
            self.fields["deadline"] = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.now().date()}))
            self.fields["assigned_to"].queryset = members
            self.fields["project"].queryset = projects
            del self.fields["status"]
        else:
            statuses = Status.objects.filter(organisation=user.member.organisation)
            del self.fields["title"]
            del self.fields["project"]
            del self.fields["assigned_to"]
            del self.fields["deadline"]
            del self.fields["score"]
            self.fields["status"].queryset = statuses

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )
        field_classes = {'username': UsernameField}


class TicketCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = (
            'status',
            'priority',
            'type',
        )
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        user = request.user
        statuses = Status.objects.filter(organisation=user.account)
        priorities = Priority.objects.filter(organisation=user.account)
        types = Type.objects.filter(organisation=user.account)
        super(TicketCategoryUpdateForm, self).__init__(*args, **kwargs)
        self.fields["status"].queryset = statuses
        self.fields["priority"].queryset = priorities
        self.fields["type"].queryset = types

class StatusModelForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = (
            'name',
            'test_status',
        )

class PriorityModelForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = (
            'name',
        )

class TypeModelForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = (
            'name',
        )

class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'notes',
            'file',
        )
