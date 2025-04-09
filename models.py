import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField  # For Django < 3.1; use models.JSONField in Django 3.1+

# CORE MODELS

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    logo_url = models.URLField(max_length=512, blank=True, null=True)
    additional_info = models.JSONField(blank=True, null=True)  # Use models.JSONField for Django 3.1+
    accepted_terms = models.BooleanField(default=False)
    setup_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='users')
    email = models.EmailField(max_length=255, unique=True)
    password_hash = models.TextField(blank=True, null=True)
    oauth_provider = models.CharField(max_length=50, blank=True, null=True)
    oauth_provider_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=50, default="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class Platform(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon_url = models.URLField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Integration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='integrations')
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='integrations')
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    token_expiry = models.DateTimeField(blank=True, null=True)
    scopes = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.platform.name} integration for {self.organization.name}"


class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='employees')
    external_employee_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    is_anonymized = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# EXTRACTED DATA MODELS

class MsCalendarEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='ms_calendar_events')
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name='ms_calendar_events')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, related_name='ms_calendar_events', blank=True, null=True)
    event_id = models.CharField(max_length=255)
    tenant_id = models.CharField(max_length=255)
    organizer = models.CharField(max_length=255)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    attendees = models.JSONField(blank=True, null=True)
    virtual = models.BooleanField(default=False)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    date_extracted = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class MsDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='ms_documents')
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name='ms_documents')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, related_name='ms_documents', blank=True, null=True)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100, blank=True, null=True)
    user = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    date_extracted = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
        
class DocumentActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='document_activities')
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name='document_activities')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, related_name='document_activities', blank=True, null=True)
    activity_id = models.CharField(max_length=255, unique=True)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    date_extracted = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} by {self.user_name}"

class MsEmail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='ms_emails')
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name='ms_emails')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, related_name='ms_emails', blank=True, null=True)
    platform = models.CharField(max_length=50, default="microsoft_365")
    user_upn = models.CharField(max_length=255)
    email_id = models.CharField(max_length=255, unique=True)
    subject = models.TextField(blank=True, null=True)
    sent_from = models.CharField(max_length=255, blank=True, null=True)
    sent_to = models.TextField(blank=True, null=True)
    reply_to = models.CharField(max_length=255, blank=True, null=True)
    conversation_id = models.CharField(max_length=255, blank=True, null=True)
    received_at = models.DateTimeField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    date_extracted = models.DateTimeField()
    full_body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject if self.subject else self.email_id


class TeamsChat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='teams_chats')
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name='teams_chats')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, related_name='teams_chats', blank=True, null=True)
    chat_id = models.CharField(max_length=255, unique=True)
    from_user = models.CharField(max_length=255)
    channel_name = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    thread_id = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.chat_id} from {self.from_user}"
