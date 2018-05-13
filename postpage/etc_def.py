from authpage.models import SCHEDULE

#아래코드에서... 
#반복문을 통해 역참조 기능이 불가능해서 대책으로
#user.id를 통해 스케쥴 쿼리셋을 취득해온다.
#취득시 해당 유저에 1개씩 밖에 없으므로 길이를 통해 스케쥴 있는사람과 없는사람을 구분하고
#스케쥴 설정을 하지 않은 유저목록은 따로 생성해주고
#스케쥴 있는 유저 시간을 합쳐준다.
def time_combine(list):
    result ={} #결과 저장할 사전
    schedule = [] #전체 스케쥴
    result['noschedule']=[] #스케쥴이 없는 유저 정보

    for user in list:
        time = SCHEDULE.objects.filter(user_id=user.id)
        if len(time)==0:
            #쿼리셋 길이가 0인 유저는 스케쥴 정보가 없는 유저이므로
            #스케쥴 없는 사람 리스트에 추가한다.
            result['noschedule'].append(user)
        else:
            #가져온건 쿼리셋 정보이므로 튜플들의 정보를 가지고있을뿐이다... 따라서 인덱스 접근으로 
            schedule += time[0].time.split(',')
    result['schedule']=schedule
    return result

def count(obj):
    remove_overlap = list(set(obj))
    dic = {}
    for list_name in remove_overlap:
        dic[list_name] = 0
    for list_count in obj:
        dic[list_count] = dic[list_count] + 1
    return dic

def en_to_ko(text):
    for i in range(0,len(text)):
        if text[i] == 'mo1':
            text[i] = ['월',1]
        elif text[i] == 'mo2':
            text[i] = ['월',2]
        elif text[i] == 'mo3':
            text[i] = ['월',3]
        elif text[i] == 'mo4':
            text[i] = ['월',4]
        elif text[i] == 'mo5':
            text[i] = ['월',5]
        elif text[i] == 'mo6':
            text[i] = ['월',6]
        elif text[i] == 'tu1':
            text[i] = ['화',1]
        elif text[i] == 'tu2':
            text[i] = ['화',2]
        elif text[i] == 'tu3':
            text[i] = ['화',3]
        elif text[i] == 'tu4':
            text[i] = ['화',4]
        elif text[i] == 'tu5':
            text[i] = ['화',5]
        elif text[i] == 'tu6':
            text[i] = ['화',6]
        elif text[i] == 'we1':
            text[i] = ['수',1]
        elif text[i] == 'we2':
            text[i] = ['수',2]
        elif text[i] == 'we3':
            text[i] = ['수',3]
        elif text[i] == 'we4':
            text[i] = ['수',4]
        elif text[i] == 'we5':
            text[i] = ['수',5]
        elif text[i] == 'we6':
            text[i] = ['수',6]
        elif text[i] == 'th1':
            text[i] = ['목',1]
        elif text[i] == 'th2':
            text[i] = ['목',2]
        elif text[i] == 'th3':
            text[i] = ['목',3]
        elif text[i] == 'th4':
            text[i] = ['목',4]
        elif text[i] == 'th5':
            text[i] = ['목',5]
        elif text[i] == 'th6':
            text[i] = ['목',6]
        elif text[i] == 'fr1':
            text[i] = ['금',1]
        elif text[i] == 'fr2':
            text[i] = ['금',2]
        elif text[i] == 'fr3':
            text[i] = ['금',3]
        elif text[i] == 'fr4':
            text[i] = ['금',4]
        elif text[i] == 'fr5':
            text[i] = ['금',5]
        elif text[i] == 'fr6':
            text[i] = ['금',6]
        elif text[i] == 'sa1':
            text[i] = ['토',1]
        elif text[i] == 'sa2':
            text[i] = ['토',2]
        elif text[i] == 'sa3':
            text[i] = ['토',3]
        elif text[i] == 'sa4':
            text[i] = ['토',4]
        elif text[i] == 'sa5':
            text[i] = ['토',5]
        elif text[i] == 'sa6':
            text[i] = ['토',6]
        elif text[i] == 'su1':
            text[i] = ['일',1]
        elif text[i] == 'su2':
            text[i] = ['일',2]
        elif text[i] == 'su3':
            text[i] = ['일',3]
        elif text[i] == 'su4':
            text[i] = ['일',4]
        elif text[i] == 'su5':
            text[i] = ['일',5]
        elif text[i] == 'su6':
            text[i] = ['일',6]
    return text

def blank_time_combin(text):
    text = en_to_ko(text)
    result = {'월':'','화':'','수':'','목':'','금':'','토':'','일':'', }
    for day_set in text:
        if day_set[0] =='월':
            result['월']+=str(day_set[1])
        elif day_set[0] =='화':
            result['화']+=str(day_set[1])
        elif day_set[0] =='수':
            result['수']+=str(day_set[1])
        elif day_set[0] =='목':
            result['목']+=str(day_set[1])
        elif day_set[0] =='금':
            result['금']+=str(day_set[1])
        elif day_set[0] =='토':
            result['토']+=str(day_set[1])
        elif day_set[0] =='일':
            result['일']+=str(day_set[1])
    
    if len(result['월'])== 0:
        del result['월']
    elif len(result['화'])==0:
        del result['화']
    elif len(result['수'])==0:
        del result['수']
    elif len(result['목'])==0:
        del result['목']
    elif len(result['금'])==0:
        del result['금']
    elif len(result['토'])==0:
        del result['토']
    elif len(result['일'])==0:
        del result['일']
    return result
