import * as commonItem from "./commonItem.js"

commonItem.printCommonItem([]);

function makeNewsText(jsonData){

    let text = "<li><div class=\"el_newsContent\"><time datetime=\"";
    text += jsonData["date"].substring(0, 4) + "-" + jsonData["date"].substring(5, 7) + "-" + jsonData["date"].substring(8, 10);
    text += "\">" + jsonData["date"] + "：</time>";
    text += "<p>" + jsonData["text"] + "</p></div></li>";

    return text;

}

fetch("./json/news.json")
    .then(function (response){
        return response.json();
    })
    .then(function (data){
        const newsList = document.querySelector("#newsList");
        let text = "";
        for(let i = 0; i < 5; i++){
            if(i < data.length){
                text += makeNewsText(data[i]);
            }
        };
        newsList.innerHTML = text;
    });