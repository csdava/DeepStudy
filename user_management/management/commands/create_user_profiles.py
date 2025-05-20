from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from user_management.models import UserProfile

class Command(BaseCommand):
    help = 'Creates UserProfile for existing users'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            if not hasattr(user, 'userprofile'):
                # 如果用户名包含'teacher'，设置为教师角色
                role = 'teacher' if 'teacher' in user.username.lower() else 'student'
                UserProfile.objects.create(user=user, role=role)
                self.stdout.write(self.style.SUCCESS(f'Created {role} profile for {user.username}')) 