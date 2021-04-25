

document.getElementById("english_button").onclick = function() {
    window.alert("404 Error.\nこんなページはないよ！");
}

function initialize_common_section(){
    var id = document.getElementById('return');
    
    id.innerHTML = '<nav><ul><li><a href="#header">Topに戻る</a></li><li><a href="#" id="english_button">English</a></li></ul></nav>'
}



initialize_common_section();

