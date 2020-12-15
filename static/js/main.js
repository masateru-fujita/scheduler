var add_btn = document.getElementById('add-btn');
var form = document.getElementById('form-wrap');
var hover_area = document.getElementById('hover-area');

add_btn.addEventListener('click', () => {
    $("#form-wrap").stop(true).animate({'width': 'toggle'});
    $("#add-btn").css({"display": "none"});
});

// コンテンツを非表示
$('#close-form-btn').on('click', function () { // 表示されたコンテンツをクリックで削除
    $("#form-wrap").css({"display": "none"});
    $("#add-btn").css({"display": "block"});
});