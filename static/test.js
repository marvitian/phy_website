

let json;
let scenario;

let x;

window.onload = function(){
    call_getx();
    call_get_scenario();
}


async function call_getx(){
    let response = await fetch('/getx');

    if ( response.ok ) {
        let json = await response.json();
        document.getElementById("filler").innerHTML = JSON.stringify(json);
        
    } else{
        alert("HTTP ERROR");
    }
}


async function call_get_scenario(){
    let response = await fetch('/get_scenario');

    if ( response.ok ) {
        let scenario = await response.text();
        document.getElementById("scenario").innerHTML = scenario;

    } else{
        alert("HTTP ERROR");
    }
}

// experimental fetch usage: from meeting 

async function setscenario(value){
    console.log(value);
    let response = await fetch(
        '/scenario', 
        {
            method: 'POST',
            body: value
        }
    );
    if ( response.ok ){
        call_get_scenario();
    }
    
}

