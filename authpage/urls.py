from django.urls import path
from django.contrib.auth.forms import AuthenticationForm
from authpage import views
from django.contrib.auth.views import login
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    #page
    path ('',views.home, name="home"), # 대문
    path ('index/',views.index, name="index"), #소개 페이지

    #auth
    path('signin/',views.sign_in, name="sign_in"), #로그인
    path('logout/', auth_views.logout, name='logout', kwargs={'next_page':settings.LOGIN_URL}), #로그아웃 
    path('sign_up/',views.sign_up, name="sign_up"), #회원가입 

    #settings 
    path('chanage/',views.change_password, name='change_password'), #비밀번호 변경
    path('<pk>/destroy/',views.user_destroy, name="destroy"), #탈퇴
    path('settings/',views.view_settings, name="settings"), # 설정 보여주기
    path('settings/update',views.settings, name="settings_update"), #설정 업데이트
]