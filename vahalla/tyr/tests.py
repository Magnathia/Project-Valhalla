from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import UserSpace, UserGroup, GroupMembership

class UserModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpassword'))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

class UserSpaceModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.user_space = UserSpace.objects.create(user=self.user)

    def test_user_space_creation(self):
        self.assertEqual(str(self.user_space), "testuser's User Space")

    def test_get_user(self):
        user = self.user_space.get_user()
        self.assertEqual(user, self.user)

class UserGroupModelTest(TestCase):
    def setUp(self):
        self.group = UserGroup.objects.create(name='Test Group')

    def test_user_group_creation(self):
        self.assertEqual(str(self.group), 'Test Group')

class GroupMembershipModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.group = UserGroup.objects.create(name='Test Group')
        self.membership = GroupMembership.objects.create(user=self.user, group=self.group)

    def test_group_membership_creation(self):
        self.assertEqual(self.membership.user, self.user)
        self.assertEqual(self.membership.group, self.group)

    def test_get_user(self):
        user = self.membership.get_user()
        self.assertEqual(user, self.user)

    def test_get_group(self):
        group = self.membership.get_group()
        self.assertEqual(group, self.group)
