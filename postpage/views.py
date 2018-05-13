from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from postpage.forms import PostForm
from postpage.models import Post,Use
from authpage.models import SCHEDULE
from django.http import JsonResponse
from postpage.etc_def import count, time_combine, blank_time_combin
import operator
from django.core.paginator import Paginator

#POST 전체 리스트
@login_required
def post_list(request):
    #데이터 가져오기
    post_list = Post.objects.all() #전체 게시글 가져오기
    search = request.GET.get('search',None) #검색 가져오기
    
    #검색소스
    if search is not None: #검색이 있다면 
        post_list = Post.objects.filter(title__contains=search) #필터해서 적용
    
    #페이지 네이션
    paginator = Paginator(post_list, 6) #6개씩 묶어 페이지 생성 선언
    page = request.GET.get('page',1 )
    try:
        paginator = paginator.page(page)
    except PageNotAnInteger:
        paginator = paginator.page(1)
    except EmptyPage:
        paginator = paginator.page(paginator.num_pages)

    context= {'post_list':paginator,}
    return render(request, 'postpage/post_list.html',context)

#내 POST 리스트
@login_required
def my_post_list(request):
    my_post = [use.post for use in Use.objects.all().filter(user_id=request.user.id)]
    search = request.GET.get('search', None)
    if  search is not None: #검색
        #필터에서 역참조 위해서는 해당 역참조 모델 소문자__속성명__규칙(contains: 포함 모든 등!)=값 이다.
        my_post = [use.post for use in Use.objects.all().filter(user_id=request.user.id, post__title__contains=search)]

    #페이지 네이션
    paginator = Paginator(my_post, 6) #6개씩 묶어 페이지 생성 선언

    page = request.GET.get('page',1 )
    try:
        paginator = paginator.page(page)
    except PageNotAnInteger:
        paginator = paginator.page(1)
    except EmptyPage:
        paginator = paginator.page(paginator.num_pages)

    context= {'post_list':paginator}
    return render(request, 'postpage/my_post_list.html',context)

#모임 개설
@login_required
def post_edit(request):
    if request.method == 'POST': #post 요청을 받을때
        form = PostForm(request.POST) #게시글 폼 내용을 받아서
        if form.is_valid(): # 유효성 검증하고 유효하다면
            post=form.save(commit=False) #필드 내용들을 채운 후 post인스턴스를 리턴
            post.author_id=request.user.id #작성자 필드를 채우고
            post.save() #세이브한다.
            #아래 코드는 save위에서 쓸때 에러가 발생한다. 이유는 post는 아직 세이브전인데 
            #해당 post의 id를 집어넣어야하기 때문이며 따라서 무조건 post가 db에 적용된 후 작성 해줘야한다.
            #아래 코드는 참여인원 체크를 위한 작업이다.
            post.use_set.create(post_id=post.id,user_id=request.user.id) 
            return redirect('post_list')
    else: #다른 방식으로 요청이 들어오면 빈 폼을 보여준다.
        form=PostForm()
    context= {'form':form}
    return render(request, 'postpage/post_edit.html', context)

#모임 페이지
@login_required
def post_view(request,pk):
    post = Post.objects.get(pk=pk) #먼저 게시글에 대한 정보를 가져온다.
    user_list = [use.user for use in request.user.use_set.all()]
    context= {'post':post}
    return render(request, 'postpage/post_view.html',context)



#모임 체크 위한 ajax 뷰
def post_schedule(request):
    #스케쥴 전체 시간
    free = ['mo1', 'tu1', 'we1', 'th1', 'fr1', 'sa1', 'su1', 'mo2', 'tu2', 'we2', 'th2', 'fr2', 'sa2', 'su2', 'mo3', 'tu3', 'we3', 'th3', 'fr3', 'sa3', 'su3', 'mo4', 'tu4', 'we4', 'th4', 'fr4', 'sa4', 'su4', 'mo5', 'tu5', 'we5', 'th5', 'fr5', 'sa5', 'su5', 'mo6', 'tu6', 'we6', 'th6', 'fr6', 'sa6', 'su6']
    if request.method == 'POST': #요청 메소드가 POST이고
        if request.is_ajax(): #ajax 통신으로 요청했을 경우
            pk = request.POST.get('pk', None) #pk라는 변수로 post의 pk를 받아
            post = Post.objects.get(pk=pk) #해당 인스턴스 모임글을 찾는다.

            #데이터 전처리
            user_list = [use.user for use in post.use_set.all()] #모임글에서 유저들의 정보 가져오기
            data = time_combine(user_list) # data 변수는 스케쥴 없는 유저정보, 사용중 시간을 종합한 데이터
            time = count(data['schedule']) # time 변수는 중복되는 시간을 가진 데이터

            #실제 활용할 변수들
            noschedule= data['noschedule'] # noschedule 변수는 스케쥴이 없는 유저 데이터를 가진다.
            sorted_time = sorted(time.items() , key=operator.itemgetter(1), reverse=True) # sorted_time 변수는 우선순위 부여한다.
            
            free = sorted([t for t in free if t not in data['schedule'] ]) # free 변수는 공강 데이터를 가진다.
            free = blank_time_combin(free) # 변수 태그명을 한글로 변경하고 시간을 합친다.

            context = {'noschedule':noschedule,'sorted_time':sorted_time,'free':free }

            rank1= []
            rank2= []
            rank3= []
            for num in sorted_time:
                if num[1] == 1:
                    rank1.append(num[0])
                if num[1] == 2:
                    rank2.append(num[0])
                if num[1] == 3:
                    rank3.append(num[0])
            print(rank1)
            rank1 = blank_time_combin(rank1)
            print(rank1)
            if len(rank1) >= 3:
                context['rank1'] = rank1
                return JsonResponse(context)
            if len(rank1) < 3:
                rank2 = blank_time_combin(rank2)
                if len(rank1)+len(rank2) > 3 :
                    context['rank1'] = rank1
                    context['rank2'] = rank2
                    return JsonResponse(context)
                else:
                    rank3 = blank_time_combin(rank3)
                    if len(rank3) > 1:
                        context['rank3'] = rank3
                    else:
                        context['rankNo'] = "3명이상 겹칩니다."
                        return JsonResponse(context)

            return JsonResponse(context)
            

#모달 반복 제거위해 사용하는 함수
def modal(request, template='news/post_modal.html'):
    pk = request.POST.get('pk', None)
    post = Post.objects.get(pk=pk)
    return render(request,'postpage/post_modal.html', {'post':post})


#모달 send 받는 뷰 함수 
def password_check(request,pk):
    #모달 상태에서 패스워드 체크
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        password= request.POST.get('password', None)
        user=request.user.use_set.filter(post_id=pk)
        
        print(password)
        print(post.password)
        if password == post.password:
            if not user: #등록이 되어 있지 않다면
                post.use_set.create(post_id=post.id,user_id=request.user.id)
            print("실행문의")
            return JsonResponse({'result':'{}/post/'.format(pk)})
    return JsonResponse({'result':'비밀번호가틀렸습니다'})