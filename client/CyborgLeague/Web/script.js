function disableButton(element){
    element.disabled = true;
}

function enableButton(element){
    element.disabled = false;
}

function shutdown(){
    pywebview.api.shutdown()
}

function minimize(){
    pywebview.api.minimize()
}

function refreshSettings(){
    apibase = "http://127.0.0.1:34850/api/v1/getSetting/"
    client_LoL_loc = get(apibase+"client_LoL_loc");
    server_api_loc = get(apibase+"server_api_loc");
    selected_champ = get(apibase+"selected_champ");

    selected_champ_element = document.getElementById("selected_champ")
    client_LoL_loc_element = document.getElementById("client_LoL_loc")
    server_api_loc_element = document.getElementById("server_api_loc")

    client_LoL_loc_element.value = client_LoL_loc
    server_api_loc_element.value = server_api_loc
    selected_champ_element.value = selected_champ
}

function browseFolder(){
    input = document.getElementById("client_LoL_loc")
    input.value = get("/api/v1/browse")
}

function updateSettings(){
    client_LoL_loc_element = encodeURIComponent(document.getElementById("client_LoL_loc").value)
    server_api_loc_element = encodeURIComponent(document.getElementById("server_api_loc").value)
    selected_champ_element = encodeURIComponent(document.getElementById("selected_champ").value)

    apibase = "http://127.0.0.1:34850/api/v1/setSetting/"
    client_LoL_loc = get(apibase+"client_LoL_loc?value="+client_LoL_loc_element);
    server_api_loc = get(apibase+"server_api_loc?value="+server_api_loc_element);
    selected_champ = get(apibase+"selected_champ?value="+selected_champ_element);

    refreshSettings();
}

function get(url){
    value = null
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, false);
    xhr.onload = function (e) {
    if (xhr.readyState === 4) {
        if (xhr.status === 200) {
            value = xhr.responseText;
        } else {
            alert(xhr.responseText)
        }
    }
    };
    xhr.onerror = function (e) {
        console.error(xhr.statusText);
    };
    try{
        xhr.send(null);
    }catch(e){
        alert(e)
        alert(url)
    }
    return value
}


function checkSettings(){
    try{
        checkapi_base = "http://127.0.0.1:34850/api/v1/checkSettings"
        check = JSON.parse(get(checkapi_base));
        if (check["client_loc"] != true){
            createPopup("CyborgLeague","League of Legends was not found. Check your `League of Legends Path` in settings")
            return
        }
        if (check["client_running"] != true){
            createPopup("CyborgLeague","League of Legends doesn't seem to be running. Maybe its set path in settings is wrong?")
            return
        }
        if (check["server"] != true){
            createPopup("CyborgLeague","The CyborgLeague server wasn't found. Check that it is running and check your settings to make sure its URL is correct.")
            return
        }
        return check["server"] && check["client_running"] && check["client_loc"]
    }catch(e){
        alert(e)
        return false
    }
}

function createPopup(title, text){
    html = '<div class="popup"> <div class="popup_content"> <p class="title">'+title+'</p><br>'+text+'<div class="bottom_menu"> <button class="button close-popup is-secondary">Ok</button> </div></div></div>'
    document.getElementById("popups_area").innerHTML = html
    document.getElementsByClassName("close-popup")[0].onclick = function (){
        deletePopup();
        openSettings();
    }
}

function deletePopup(){
    document.getElementById("popups_area").innerHTML = ''
}

function initialize_profile(){
    let username = "";
    let level = "";
    const level_element = document.getElementById("level");
    const username_element = document.getElementById("username");

    fetch("http://127.0.0.1:34850/api/v1/getSummonerName")
    .then(response => response.text())
    .then((response) => {
        username = response;
        username_element.innerHTML = username;
    }).catch(error => {alert(error);});

    fetch("http://127.0.0.1:34850/api/v1/getSummonerLevel")
    .then(response => response.text())
    .then((response) => {
        level = response;
        level_element.innerHTML = level;
    }).catch(error => {alert(error);});
}

function waitUntilApiUp(){
    let status = false
    while (!status){
        try{
            fetch("http://127.0.0.1:34850/status");
            status = true;
        }
        catch(e){
            status = false;
        }
    }
    return status;
}

CyborgLeagueWrapper = {
    "helpers":{
        "UpdateStatus": function(){
            CyborgLeagueWrapper.status(function(status){
                if(status == "false"){
                    CyborgLeagueWrapper.helpers.StoppedStatusUpdate();
                }else{
                    CyborgLeagueWrapper.helpers.StartedStatusUpdate();
                }
            })
            CyborgLeagueWrapper.helpers.StoppedStatusUpdate();
        },
        "StartedStatusUpdate": function(){
            disableButton(document.getElementById("OnButton"))
            enableButton(document.getElementById("OffButton"));
            document.getElementById("OnButton").textContent = "Bot Started"
        },
        "StoppedStatusUpdate": function(){
            disableButton(document.getElementById("OffButton"));
            enableButton(document.getElementById("OnButton"));
            document.getElementById("OnButton").textContent = "Start Bot"
        },
        "OnButtonClicked": function(){
            CyborgLeagueWrapper.start();
        },
        "OffButtonClicked": function(){
            CyborgLeagueWrapper.stop();
        }
    },
    "start": function() {
        if (!checkSettings()){
            return;
        }
        fetch("http://127.0.0.1:34850/api/v1/start")
        .then((response) => response.json())
        .then((responseJson) => {
            CyborgLeagueWrapper.helpers.StartedStatusUpdate();
            initialize_profile();
        });
            
    },
    "stop":  function()  {
        fetch("http://127.0.0.1:34850/api/v1/stop")
        .then((response) => response.json())
        .then((responseJson) => {
            CyborgLeagueWrapper.helpers.StoppedStatusUpdate();
        })
    },
    "status":  function(callback)  {
        fetch('http://127.0.0.1:34850/status')
            .then(response => response.text())
            .then(data => callback(data));
    },
    "toggle": function(){
        CyborgLeagueWrapper.status(function(status){
            if(status == "true"){
                CyborgLeagueWrapper.stop();
            }else{
                CyborgLeagueWrapper.start();
                
            }
        });
    }
}

waitUntilApiUp();

refreshSettings();

document.getElementById("OnButton").onclick = CyborgLeagueWrapper.helpers.OnButtonClicked;
document.getElementById("OffButton").onclick = CyborgLeagueWrapper.helpers.OffButtonClicked;

function getHelp(){
    window.open('https://github.com/bastien8060/CyborgLeague/wiki')
}
