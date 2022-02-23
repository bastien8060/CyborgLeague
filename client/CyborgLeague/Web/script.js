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

waitUntilApiUp();
initialize_profile();
