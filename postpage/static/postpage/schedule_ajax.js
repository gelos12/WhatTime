function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(window).on("load", function () {
    // Handler when all assets (including images) are loaded

    var pk = $('#hidden_pk').attr('name')
    var url = $('#hidden_pk').val()
    var csrf = getCookie("csrftoken");


    $.ajax({
        type: 'post', // post방식으로 전송
        url: url, // 서버로 보낼 url 주소
        data: {  // 서버로 보낼 데이터들 dict형식
            'pk': pk,
            'csrfmiddlewaretoken': csrf,
        },
        // dataType : 'html',
        // 서버에서 리턴받아올 데이터 형식
        dataType: 'json',
        //서버에서 무사히 html을 리턴하였다면 실행
        success: function (data, textStatus, jqXHR) {

            //스케쥴 표시
            $(data['sorted_time']).each(function (index) {
                $('#' + data['sorted_time'][index][0]).css(
                    'background-color', '#e3f2fd'
                )
            });

            //조율 순위 
            console.log(data)
            if(data.hasOwnProperty('rank1')){
                var rank1= data['rank1']
                if (rank1.hasOwnProperty('월')){
                    $("#mo_rank_time").remove()
                    $("#tunig_list").append('<li><a id="mo_rank_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"1명,"+'월'+rank1['월']+'</a></li>')
                }
                if (rank1.hasOwnProperty('화')){
                    $("#tu_rank_time").remove()
                    $("#tunig_list").append('<li><a id="tu_rank_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"1명,"+'화'+rank1['화']+'</a></li>')
                }
                if (rank1.hasOwnProperty('수')){
                    $("#we_rank_time").remove()
                    $("#tunig_list").append('<li><a id="we_rank_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"1명,"+'수'+rank1['수']+'</a></li>')
                }
                if (rank1.hasOwnProperty('목')){
                    $("#th_rank_time").remove()
                    $("#tunig_list").append('<li><a id="th_rank_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"1명,"+'목'+rank1['목']+'</a></li>')
                }
                if (rank1.hasOwnProperty('금')){
                    $("#fr_rank_time").remove()
                    $("#tunig_list").append('<li><a id="fr_rank_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"1명,"+'금'+rank1['금']+'</a></li>')
                }
                if (rank1.hasOwnProperty('토')){
                    $("#sa_rank_time").remove()
                    $("#tunig_list").append('<li><a id="sa_rank_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"1명,"+'토'+rank1['토']+'</a></li>')
                }
                if (rank1.hasOwnProperty('일')){
                    $("#su_rank_time").remove()
                    $("#tunig_list").append('<li><a id="su_rank_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"1명,"+'일'+rank1['일']+'</a></li>')
                }
            }
            if(data.hasOwnProperty('rank2')){
                var rank2= data['rank2']
                if (rank2.hasOwnProperty('월')){
                    $("#mo_rank2_time").remove()
                    $("#tunig_list").append('<li><a id="mo_rank2_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"2명,"+'월'+rank2['월']+'</a></li>')
                }
                if (rank2.hasOwnProperty('화')){
                    $("#tu_rank2_time").remove()
                    $("#tunig_list").append('<li><a id="tu_rank2_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"2명,"+'화'+rank2['화']+'</a></li>')
                }
                if (rank2.hasOwnProperty('수')){
                    $("#we_rank2_time").remove()
                    $("#tunig_list").append('<li><a id="we_rank2_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"2명,"+'수'+rank2['수']+'</a></li>')
                }
                if (rank2.hasOwnProperty('목')){
                    $("#th_rank2_time").remove()
                    $("#tunig_list").append('<li><a id="th_rank2_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"2명,"+'목'+rank2['목']+'</a></li>')
                }
                if (rank2.hasOwnProperty('금')){
                    $("#fr_rank2_time").remove()
                    $("#tunig_list").append('<li><a id="fr_rank2_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"2명,"+'금'+rank2['금']+'</a></li>')
                }
                if (rank2.hasOwnProperty('토')){
                    $("#sa_rank2_time").remove()
                    $("#tunig_list").append('<li><a id="sa_rank2_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"2명,"+'토'+rank2['토']+'</a></li>')
                }
                if (rank2.hasOwnProperty('일')){
                    $("#su_rank2_time").remove()
                    $("#tunig_list").append('<li><a id="su_rank2_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"2명,"+'일'+rank2['일']+'</a></li>')
                }
            }
            if(data.hasOwnProperty('rank3')){
                var rank3= data['rank3']
                if (rank3.hasOwnProperty('월')){
                    $("#mo_rank3_time").remove()
                    $("#tunig_list").append('<li><a id="mo_rank3_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"3명,"+'월'+rank3['월']+'</a></li>')
                }
                if (rank3.hasOwnProperty('화')){
                    $("#tu_rank3_time").remove()
                    $("#tunig_list").append('<li><a id="tu_rank3_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"3명,"+'화'+rank3['화']+'</a></li>')
                }
                if (rank3.hasOwnProperty('수')){
                    $("#we_rank3_time").remove()
                    $("#tunig_list").append('<li><a id="we_rank3_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"3명,"+'수'+rank3['수']+'</a></li>')
                }
                if (rank3.hasOwnProperty('목')){
                    $("#th_rank3_time").remove()
                    $("#tunig_list").append('<li><a id="th_rank3_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"3명,"+'목'+rank3['목']+'</a></li>')
                }
                if (rank3.hasOwnProperty('금')){
                    $("#fr_rank3_time").remove()
                    $("#tunig_list").append('<li><a id="fr_rank3_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"3명,"+'금'+rank3['금']+'</a></li>')
                }
                if (rank3.hasOwnProperty('토')){
                    $("#sa_rank3_time").remove()
                    $("#tunig_list").append('<li><a id="sa_rank3_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"3명,"+'토'+rank3['토']+'</a></li>')
                }
                if (rank3.hasOwnProperty('일')){
                    $("#su_rank3_time").remove()
                    $("#tunig_list").append('<li><a id="su_rank3_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"3명,"+'일'+rank3['일']+'</a></li>')
                }
            }
            if(data.hasOwnProperty('rankNo')){
                var rankNo= data['rankNo']
                $("#tunig_list").append('<li><a id="su_rank3_time" class="btn btn-xs btn-primary btn-outlined" href="#">'+"3명이상 겹칩니다."+'</a></li>')
            }
            
            //공강시간 
            var free = data['free']
            if (free.hasOwnProperty('월')){
                $("#mo_free").remove()
                $("#free_time").append("<span id='mo_free'>"+"월"+free['월']+"</span>")
            }
            if (free.hasOwnProperty('화')){
                $("#tu_free").remove()
                $("#free_time").append("<br><span id='tu_free'>"+"화"+free['화']+"</span>")
            }
            if (free.hasOwnProperty('수')){
                $("#we_free").remove()
                $("#free_time").append("<br><span id='we_free'>"+"수"+free['수']+"</span>")
            }
            if (free.hasOwnProperty('목')){
                $("#th_free").remove()
                $("#free_time").append("<br><span id='th_free'>"+"목"+free['목']+"</span>")
            }
            if (free.hasOwnProperty('금')){
                $("#fr_free").remove()
                $("#free_time").append("<br><span id='fr_free'>"+"금"+free['금']+"</span>")
            }
            if (free.hasOwnProperty('토')){
                $("#sa_free").remove()
                $("#free_time").append("<br><span id='sa_free'>"+"토"+free['토']+"</span>")
            }
            if (free.hasOwnProperty('일')){
                $("#su_free").remove()
                $("#free_time").append("<span id='su_free'>"+"일"+free['일']+"</span>")
            }

            
        },

        //서버에서 html을 리턴해주지 못했다면
        error: function (data, textStatus, jqXHR) {

        },

    });
});


