import * as commonItem from "./commonItem.js"

commonItem.printCommonItem(["work"]);


function makeConferenceText(jsonData){

    let text = "<li><p>" + jsonData["author"] + "，<br>";
    text += "\"" + jsonData["title"] +"\"，<br>";

    const conferenceList = ["conference", "volume", "state", "date", "style"];

    for(const key in conferenceList){
        if(conferenceList[key] in jsonData){
            if(conferenceList[key] === "volume"){
                jsonData[conferenceList[key]] = "Vol." + jsonData[conferenceList[key]];
            }
            text += jsonData[conferenceList[key]] + "，";
        };
    }

    if("status" in jsonData && jsonData["status"] === "accepted"){
        text += "（発表受理），"
    }
    if("prize" in jsonData){
        text += "<br><span class=\"hp_attention\">" + jsonData["prize"] + "</span>，"
    }

    text = text.slice(0, -1);
    text += "．</p></li>"
    
    return text;

}

fetch("./json/work/conference.json")
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        const ol_id = document.querySelector("#conference");
        ol_id.style.counterReset = "ol " + String(data.length+1);
        let text = "";
        for(let i = 0; i < data.length; i++){
            text += makeConferenceText(data[i]);
        };
        ol_id.innerHTML = text;
    });
