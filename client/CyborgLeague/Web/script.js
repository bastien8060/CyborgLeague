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
            CyborgLeagueWrapper.helpers.StartedStatusUpdate();
        },
        "OffButtonClicked": function(){
            CyborgLeagueWrapper.stop();
            CyborgLeagueWrapper.helpers.StoppedStatusUpdate();
        }
    },
    "start": function() {
        fetch("http://127.0.0.1:34850/api/v1/start");
    },
    "stop":  function()  {
        fetch("http://127.0.0.1:34850/api/v1/stop");
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
                document.getElementById("OnOffButton").textContent = "Start Bot";
            }else{
                CyborgLeagueWrapper.start();
                document.getElementById("OnOffButton").textContent = "Stop Bot";
            }
        });
    }
}

waitUntilApiUp();
initialize_profile();

document.getElementById("OnButton").onclick = CyborgLeagueWrapper.helpers.OnButtonClicked;
document.getElementById("OffButton").onclick = CyborgLeagueWrapper.helpers.OffButtonClicked;

CyborgLeagueWrapper.helpers.UpdateStatus();


