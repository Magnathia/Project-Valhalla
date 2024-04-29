from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class CustomUser(AbstractUser):
    # Custom fields
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'username': self.username})

    def get_profile(self):
        return self.profile_set.first()

class UserSpace(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_space')

    def __str__(self):
        return f"{self.user.username}'s User Space"

    def get_user(self):
        return self.user

    def get_user_profile(self):
        return self.user.profile_set.first()

    def update_profile_picture(self, new_picture):
        self.user.profile_picture = new_picture
        self.user.save()

    def update_bio(self, new_bio):
        self.user.bio = new_bio
        self.user.save()

    def update_website(self, new_website):
        self.user.website = new_website
        self.user.save()

class UserGroup(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    def add_user(self, user):
        self.groupmembership_set.create(user=user)

    def remove_user(self, user):
        self.groupmembership_set.filter(user=user).delete()

    def get_members(self):
        return [membership.user for membership in self.groupmembership_set.all()]

    def is_member(self, user):
        return self.groupmembership_set.filter(user=user).exists()

    def get_group_permissions(self):
        # Assuming you have a GroupPermission model with a foreign key to this group
        return self.grouppermission_set.all()

    def has_permission(self, permission):
        return self.grouppermission_set.filter(permission=permission).exists()


class GroupMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'group')

    def __str__(self):
        return f"{self.user} - {self.group}"

    def get_user(self):
        return self.user

    def get_group(self):
        return self.group

    @staticmethod
    def get_membership(user, group):
        try:
            return GroupMembership.objects.get(user=user, group=group)
        except GroupMembership.DoesNotExist:
            return None

    @staticmethod
    def create_membership(user, group):
        return GroupMembership.objects.create(user=user, group=group)

    @staticmethod
    def delete_membership(user, group):
        membership = GroupMembership.get_membership(user, group)
        if membership:
            membership.delete()
