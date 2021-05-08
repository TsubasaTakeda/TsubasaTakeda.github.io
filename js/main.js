function initialize_common_section(){

    /*---------------------------------------------
    ニュースを表示
    ---------------------------------------------*/
    news_url = 'json/news/2021/news_2021.json';
    $.getJSON(news_url, function getNews(data) {
        var news_id = document.getElementById('news_contents');
        var news_data = data;
        news_id.innerHTML = '';
        for (var i = 0; i < 2; i++) {
            date = '<dt>' + news_data[i].date + '</dt>';
            contents = '<dd>' + news_data[i].contents + '</dd>';
            news_id.innerHTML += date + contents;
        }
    });

    /*---------------------------------------------
    日記を表示
    ---------------------------------------------*/
    diary_url = 'json/diary/2021/diary_2021.json';
    $.getJSON(diary_url, function getNews(data) {
        var diary_id = document.getElementById('diary_contents');
        var diary_data = data;
        diary_id.innerHTML = '';
        for (var i = 0; i < 2; i++) {
            date = '<dt>' + diary_data[i].date + '</dt>';
            title = '<dd id=diary_title_' + diary_data[i].date + '>' + diary_data[i].title + '</dd>';
            diary_id.innerHTML += date + title;
        }
    });


    var id = document.getElementById('return');

    id.innerHTML = '<nav><ul><li><a href="#header">Topに戻る</a></li><li><a href="#" id="english_button">English</a></li></ul></nav>'

    footer_id = document.getElementById('footer');
    footer_id.innerHTML += '<p>最終更新日：' + document.lastModified + '</p>' 

}

initialize_common_section();


document.getElementById("english_button").onclick = function () {
    window.alert("404 Error.\nこんなページはないよ！");
}

