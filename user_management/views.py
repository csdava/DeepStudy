from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserProfileForm, UserPasswordChangeForm
from .models import UserProfile
from django.contrib import messages

def index(request):
    return render(request, 'user_management/index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, role='student')  # 默认角色为学生
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user_management/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'user_management/login.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'user_management/profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')
    else:
        form = UserPasswordChangeForm(request.user)
    return render(request, 'user_management/change_password.html', {'form': form})

@login_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'user_management/manage_users.html', {'users': users})

def role_selection(request):
    """显示身份选择页面"""
    if request.user.is_authenticated:
        if hasattr(request.user, 'userprofile'):
            if request.user.userprofile.role == 'teacher':
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            # 如果用户没有profile，创建一个默认的学生profile
            UserProfile.objects.create(user=request.user, role='student')
            return redirect('student_dashboard')
    return render(request, 'role_login.html')

@login_required
def teacher_dashboard(request):
    """教师控制台"""
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'teacher':
        messages.error(request, '您没有访问教师控制台的权限')
        return redirect('student_dashboard')
    return render(request, 'teacher_dashboard.html')

@login_required
def student_dashboard(request):
    """学生控制台"""
    if hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'teacher':
        messages.error(request, '教师不能访问学生控制台')
        return redirect('teacher_dashboard')
    return render(request, 'student_dashboard.html')

def teacher_register(request):
    """教师注册处理"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        email = request.POST.get('email', '')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在')
            return render(request, 'registration/register.html', {'role': 'teacher'})
            
        # 创建用户和教师档案
        user = User.objects.create_user(username=username, password=password, email=email)
        UserProfile.objects.create(user=user, role='teacher')
        
        messages.success(request, '注册成功！请登录')
        return redirect('teacher_login')
        
    return render(request, 'registration/register.html', {'role': 'teacher'})

def student_register(request):
    """学生注册处理"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        email = request.POST.get('email', '')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在')
            return render(request, 'registration/register.html', {'role': 'student'})
            
        # 创建用户和学生档案
        user = User.objects.create_user(username=username, password=password, email=email)
        UserProfile.objects.create(user=user, role='student')
        
        messages.success(request, '注册成功！请登录')
        return redirect('student_login')
        
    return render(request, 'registration/register.html', {'role': 'student'})

def user_logout(request):
    """处理用户登出"""
    logout(request)
    messages.success(request, '您已成功退出登录')
    return redirect('role_selection')

def teacher_login(request):
    """教师登录处理"""
    if request.user.is_authenticated:
        if hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'teacher':
            return redirect('teacher_dashboard')
        return redirect('student_dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # 如果用户没有profile，创建一个
            if not hasattr(user, 'userprofile'):
                UserProfile.objects.create(user=user, role='teacher')
            
            # 检查用户是否是教师
            if user.userprofile.role == 'teacher':
                login(request, user)
                return redirect('teacher_dashboard')
            else:
                messages.error(request, '您不是教师身份')
        else:
            messages.error(request, '用户名或密码错误')
    
    return render(request, 'registration/teacher_login.html')

def student_login(request):
    """学生登录处理"""
    if request.user.is_authenticated:
        return redirect('student_dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # 如果用户没有profile，创建一个
            if not hasattr(user, 'userprofile'):
                UserProfile.objects.create(user=user, role='student')
            
            # 检查用户是否是学生
            if user.userprofile.role == 'student':
                login(request, user)
                return redirect('student_dashboard')
            else:
                messages.error(request, '您不是学生身份')
        else:
            messages.error(request, '用户名或密码错误')
    
    return render(request, 'registration/student_login.html')