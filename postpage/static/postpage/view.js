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
// unbind().bind() 더블클릭 방지
$(document).on("click", "#send_password", addAnswer);

function addAnswer(e) {

    e.submit;
    e.stopPropagation(); // 같은 영역에 속해있는 중복 클릭 방지
    e.preventDefault();  // 이벤트 진행 중지

    password = $("#password_data").val();
    url = $("#hidden_url").val();
    var csrf = getCookie("csrftoken");


    $.ajax({
        type: 'post', // post방식으로 전송
        url: url, // 서버로 보낼 url 주소
        data: {  // 서버로 보낼 데이터들 dict형식
            'password': password,
            'csrfmiddlewaretoken': csrf,
        },
        // dataType : 'html',
        // 서버에서 리턴받아올 데이터 형식
        dataType : 'json',
        //서버에서 무사히 html을 리턴하였다면 실행
        success: function (data, textStatus, jqXHR) {
            console.log(data["result"])
            if(data["result"]=='비밀번호가틀렸습니다'){
                $("#error_p").remove()
                $("#error_list").append("<p id='error_p' class='card-text text-muted text-center' style='margin: 0 auto 0 auto'>"+data['result']+"</p>")
            }else{
                $(location).attr('href', data["result"])
            }
        },

        //서버에서 html을 리턴해주지 못했다면
        error: function (data, textStatus, jqXHR) {
            e.preventDefault();
            


        },

    });
}

