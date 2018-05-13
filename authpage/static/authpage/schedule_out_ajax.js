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

$('#scedule_save').on("click", addAnswer);
function addAnswer(e) {
  e.submit
  e.stopPropagation(); // 같은 영역에 속해있는 중복 클릭 방지
  e.preventDefault();  // 이벤트 진행 중지

  var sc = [];
  $("input[type=checkbox]:checked").each(function (i) {
    sc.push($(this).attr('name'));
  });
  // var pk = $('.check_destroy').attr('name'); //선택된 요소의 부모의 name속성 캐치
  var url = $(this).attr('url');
  var csrf = getCookie("csrftoken");

  if (sc == 0) {
    //sc가 0일때 아무작업하지 않고
  } else {
    var resend = confirm('정말로 저장하시겠습니까? 기존 자료는 모두 초기화 됩니다.');
  }

  if (resend) {
    $.ajax({
      type: 'post', // post방식으로 전송
      url: url, // 서버로 보낼 url 주소
      data: {  // 서버로 보낼 데이터들 dict형식
        sc,
        'csrfmiddlewaretoken': csrf,
      },
      // 서버에서 리턴받아올 데이터 형식
      // dataType : 'json',
      //서버에서 무사히 html을 리턴하였다면 실행
      success: function (response) {
        // location.reload();
        console.log(response)
        if (response["message"]) {
          alert("저장 되었습니다.")
          location.reload();
        } else {
          alert("실패했습니다. 관리자에게 문의주세요.");
        }
      },

      //서버에서 html을 리턴해주지 못했다면
      error: function (response) {
        alert("실패했습니다.");
      },

    });
  } else {

  }

}



$(window).on("load", function () {
  // Handler when all assets (including images) are loaded

  var url = ' '
  var csrf = getCookie("csrftoken");


  $.ajax({
    type: 'post', // post방식으로 전송
    url: url, // 서버로 보낼 url 주소
    data: {  // 서버로 보낼 데이터들 dict형식
      'csrfmiddlewaretoken': csrf,
    },
    // dataType : 'html',
    // 서버에서 리턴받아올 데이터 형식
    dataType: 'json',
    //서버에서 무사히 html을 리턴하였다면 실행
    success: function (data, textStatus, jqXHR) {

      //스케쥴 표시
      $(data['schedule']).each(function (index) {
        $('#' + data['schedule'][index]).prop('checked', true);
      });
    },

    //서버에서 html을 리턴해주지 못했다면
    error: function (data, textStatus, jqXHR) {

    },

  });
});