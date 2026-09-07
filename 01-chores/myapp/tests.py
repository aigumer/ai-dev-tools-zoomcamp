from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class UserModelTest(TestCase):

    def test_create_user_with_email(self):
        user = User.objects.create_user(email='test@example.com', username='testuser', password='pass1234')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('pass1234'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(email='admin@example.com', username='admin', password='admin1234')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_email_is_username_field(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_str_returns_email(self):
        user = User.objects.create_user(email='bob@example.com', username='bob', password='pass1234')
        self.assertEqual(str(user), 'bob@example.com')

    def test_email_must_be_unique(self):
        User.objects.create_user(email='dupe@example.com', username='user1', password='pass1234')
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email='dupe@example.com', username='user2', password='pass1234')

    def test_login_with_email(self):
        User.objects.create_user(email='login@example.com', username='loginuser', password='pass1234')
        logged_in = self.client.login(email='login@example.com', password='pass1234')
        self.assertTrue(logged_in)
