from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Comment, SocialGroup
from django.core.mail import mail_admins
from django.http import HttpResponse


class CoreBaseAdmin(admin.ModelAdmin):
    save_on_top = True


@admin.register(Post)
class PostAdmin(CoreBaseAdmin):
    list_display = ['id', 'created_by', ]
    readonly_fields = ['created_by']

    def save_model(self, request, obj, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        object_id = str(obj.id)
        sg = SocialGroup.objects.filter(posts__id__iexact=object_id)
        if change and not sg.filter.objects(user_list__id__iexact= str(request.user.pk)):
            instance.comments = obj.comments
        instance.save()
        form.save_m2m()
        return instance

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            if not instance.owner:
                instance.owner = request.user.companyemployee
            instance.save()

        super().save_formset(request, form, formset, change)

    def has_change_permission(self, request, obj=Post):
        if not obj:
            return True
        if request.user == obj.created_by:
            return True
        # sg = Post.objects.filter(pk__iexact=obj.pk).social_group_set.all()
        object_id = str(obj.id)
        sg = SocialGroup.objects.filter(posts__id__iexact=object_id)
        if sg and sg[0].admin_username == request.user:
            return True
    # def has_change_permission(self, request, obj=None):
    #     if request.user.role == 'admin':
    #         return True

@admin.register(User)
class ExtendedUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email",)}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",   #change_this to social_groups
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("username", "email", "first_name", "last_name", "is_staff", )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email", "role")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


@admin.register(SocialGroup)
class ExtendSocialGroup(CoreBaseAdmin):
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            if not instance.owner:
                instance.owner = request.user.companyemployee
            instance.save()

        super().save_formset(request, form, formset, change)

    def has_change_permission(self, request, obj=SocialGroup):
        if request.user.username == obj.admin_username:
            return True

    def has_change_permission(self, request, obj=None):
        if request.user.role == 'admin':
            return True
#
# class ExtendNotifications(Notifications):
#     pass

admin.site.register(Comment)


# Python code to illustrate Sending mail from
# your Gmail account
import smtplib
MAIL_USERNAME='elzaidh@gmail.com'
MAIL_PASSWORD='*******'
# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

# Authentication
s.login(MAIL_USERNAME, MAIL_PASSWORD)

# message to be sent
message = """

          New Post has been created, click http://127.0.0.1:8000/social/post/ to view Regards,Team Draup"""

# sending the mail
s.sendmail("elzaidh@gmail.com", "05zaidm@gmail.com", message)

# terminating the session
s.quit()
