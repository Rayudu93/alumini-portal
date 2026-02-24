from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, StudentProfile, AlumniProfile
from queries.models import Query, Answer
from events.models import Event, EventRegistration
from notifications.models import Notification


# -------------------------
# Custom User Admin
# -------------------------
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    ordering = ("email",)
    search_fields = ("email",)

    list_display = (
        "custom_id",
        "email",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    list_filter = ("role", "is_active", "is_staff")

    fieldsets = (
        (None, {"fields": ("custom_id", "email", "password", "role")}),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role", "is_active", "is_staff"),
        }),
    )

    filter_horizontal = ("groups", "user_permissions")
    readonly_fields = ("custom_id", "last_login")


# -------------------------
# Student Profile Admin
# -------------------------
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "department", "graduation_year")
    search_fields = ("user__email", "department")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role=User.STUDENT)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# -------------------------
# Alumni Profile Admin
# -------------------------
@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "company", "designation", "verified")
    search_fields = ("user__email", "company", "designation")
    list_filter = ("verified",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role=User.ALUMNI)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# -------------------------
# Queries Admin
# -------------------------
@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ("query_id","student", "title", "status", "created_at", "accepted_by")
    list_filter = ("status", "created_at")
    search_fields = ("title", "student__email", "accepted_by__email")
    ordering = ("-created_at",)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("query", "alumni", "created_at")
    list_filter = ("created_at",)
    search_fields = ("query__title", "alumni__email", "content")
    ordering = ("-created_at",)
# -------------------------
# Events Admin
# -------------------------
class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    readonly_fields = ('user', 'registered_at')
    can_delete = False

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "created_by", "registered_count")
    readonly_fields = ("registered_users",)
    search_fields = ("title", "description", "created_by__email")
    inlines = [EventRegistrationInline]

    def registered_count(self, obj):
        return obj.registered_users.count()
    registered_count.short_description = "Registered Users"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Only allow ADMIN users to be selected as the creator
        if db_field.name == "created_by":
            kwargs["queryset"] = User.objects.filter(role=User.ADMIN)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "registered_at")
    list_filter = ("event", "registered_at")
    search_fields = ("event__title", "user__email")
    ordering = ("-registered_at",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Only allow ALUMNI users for registration in admin
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role=User.ALUMNI)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# -------------------------
# Notifications Admin
# -------------------------
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user","title" ,"message")
    list_filter = ("user",)
    search_fields = ("user__email", "message")
