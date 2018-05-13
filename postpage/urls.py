from django.urls import path
from postpage import views
urlpatterns = [
    path('',views.post_list,name="post_list"), #모임 리스트
    path('lib/',views.my_post_list,name="my_post_list"), #모임 리스트

    path('edit',views.post_edit,name="post_edit"), #모임 생성
    
    path('modal/',views.modal,name="modal"), #모임 비밀번호확인 모달
    path('<int:pk>/pwcheck/',views.password_check,name="post_check"), #모임 비밀번호 확인후 작업
    
    path('<int:pk>/post/',views.post_view,name="post"), #모임보기
    path('schedule/',views.post_schedule,name="schedule"), #모임 스케쥴

    
]