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
$('#destroy').on("click", addAnswer);

function addAnswer(e) {

    e.submit;
    e.stopPropagation(); // 같은 영역에 속해있는 중복 클릭 방지
    e.preventDefault();  // 이벤트 진행 중지
    var email = $('#destroy_email').val();
    console.log(email)
    var password = $('#destroy_password').val();
    console.log(password)
    var url = $(this).attr('url');
    var resend = confirm('정말로 탈퇴하시겠습니까? 자료는 모두 제거 됩니다.');
    var csrf = getCookie("csrftoken");

    if (resend) {
        $.ajax({
            type: 'post', // post방식으로 전송
            url: url, // 서버로 보낼 url 주소
            data: {  // 서버로 보낼 데이터들 dict형식
                'resend': resend,
                'email': email,
                'password': password,
                'csrfmiddlewaretoken': csrf,
            },
            // dataType : 'html',
            // 서버에서 리턴받아올 데이터 형식

            //서버에서 무사히 html을 리턴하였다면 실행
            success: function (response) {
                console.log(response['error']);
                //append(data);
                if (response['error']) {
                    $("#error").remove()
                    $(".error_msg").append("<p id='error' class='text-center' style='margin: 0 auto 0 auto'>" + response['error'] + "</p>")
                }
                if (response["result"] == "success") {
                    alert("탈퇴 되었습니다.");
                    $(location).attr('href', "/")
                } else {

                }
            },

            //서버에서 html을 리턴해주지 못했다면
            error: function (response) {
                // console.log(response);
                e.preventDefault();
                alert("탈퇴 실패했습니다. 문의해주세요.");
            },

        });
    }
    else {

    }

}

