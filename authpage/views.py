from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .forms import UserCreationForm, LoginForm, PasswordChangeForm
from django.contrib.auth import login, get_user_model, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import SCHEDULE

#첫 대문 페이지
#@user_passes_test(lambda user : not user.is_authenticated, login_url='home')
def home(request):
    return render(request, 'authpage/home.html')

#소개 페이지
def index(request):
    return render(request, 'authpage/index.html' )

#로그인 페이지
@user_passes_test(lambda user : not user.is_authenticated, login_url='index')
def sign_in(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user= authenticate(request, username=email,password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            context = { 'error':"아이디 또는 비밀번호가 맞지 않습니다." }
            return render(request, 'authpage/sign_in.html',context)
    context = { 'error': ""}
    return render(request, 'authpage/sign_in.html', context)

#회원가입 페이지
@user_passes_test(lambda user : not user.is_authenticated, login_url='index')
def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = request.POST['email']
            password = request.POST['password1']
            user= authenticate(request, username=email,password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            context = { 'form':form }
            return render(request, 'authpage/sign_up.html',context)
    else:
        form = UserCreationForm()
    context = { 'form':form }
    return render(request, 'authpage/sign_up.html',context)

#비밀번호 변경 페이지
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('change_password')
        else:
            return render(request, 'authpage/settings_password.html', {
        'form': form
    })
    else:
        form = PasswordChangeForm(request.user,)
    return render(request, 'authpage/settings_password.html', {
        'form': form
    })
#스케쥴수정 페이지
@login_required
def view_settings(request):
    if request.method =='POST':
        if request.is_ajax():
            time = SCHEDULE.objects.filter(user_id=request.user.id)
            if len(time) == 0:
                return 0
            else:
                schedule = time[0].time.split(',')
                return JsonResponse({'schedule':schedule})
    return render(request,'authpage/settings_schedule.html')

#스케쥴설정 ajax
@login_required
def settings_ajax(request):
    user = request.user.id #유저 아이디 획득
    if reqeust.is_ajax(): # 저장했던 내용 보여주기 비동기시작
        schedule = SCHEDULE.objects.all() # 스케쥴 모든 유저들의 정보중에
        schedule = schedule.filter(user_id=user) # 해당 유저의 날짜정보를 찾는다.
        if not schedule: #만약 날짜 데이터가 없다면
            return JsonResponse({'message':False}) # 없다고 하며
        else: #있다면 가지고 있는 스케쥴 데이터를 
            time = schedule.time
            time = time.split(',') #리스트로 만들어서
            return JsonResponse({'message':True,'time':time}) #보내준다.
    return render(request,'authpage/settings.html')

#settings 설정
@login_required
def settings(request):
    user = request.user.id #유저 아이디 획득
    if request.is_ajax(): #ajax통신여부
        sc = request.POST.getlist('sc[]', None) #비동기식 통신을 통해 날짜 값을 받아온다.
        print(type(sc))
        print(sc)
        schedule = SCHEDULE.objects.all()
        schedule = schedule.filter(user_id=user)
        if not schedule: #스케쥴이 만들어져 있지 않다면
            print("스케쥴 생성작업!")
            schedule = SCHEDULE.objects.create(user_id=user, time=",".join(sc))
            return JsonResponse({'message':True})
        else: #만들어져 있다면
            schedule.update(time=",".join(sc))
            return JsonResponse({'message':True})

#탈퇴!
def user_destroy(request,pk):
 
    if request.method == 'POST': #post방식이 들어온다면
        if request.is_ajax(): #ajax라면
            
            if request.POST.get('resend', None) is not None: # 재 확인 요청을 받고
                email = request.POST.get('email') # 이메일 폼 내용을 가져오고
                password = request.POST.get('password') # 비밀번호 폼 내용을 가져온다.
                if request.user.email == email: #이때 현재 로그인 유저와 입력한 이메일이 동일하다면
                    user= authenticate(request, username=email,password=password) #입력된 값으로 인증을 진행한다.
                    if user is not None: #인증이 되었다면
                        print("들어옴")
                        print(user)
                        user = get_user_model() #유저
                        user = user.objects.get(pk=pk)
                        user.delete()
                        return JsonResponse({'result':"success"})
                    else:
                        context = { 'error':"비밀번호가 틀렸습니다." }    
                        return JsonResponse(context)
                else:
                    context = { 'error':"본인 계정과 다릅니다." }
                    return JsonResponse(context)
                
    return render(request, 'authpage/settings_destroy.html')