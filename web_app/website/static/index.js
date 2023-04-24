
function deleteNote(noteId) {
    // Takes note id that we pass and it will send a post request to the delete note endpoint, and after it gets a response it will reload the window
    fetch('/delete-note', { // To send a request in vanilla js
      method: 'POST',
      body: JSON.stringify({noteId: noteId})  
    }).then((_res) => { // then reload the window
        console.log("res = ", _res);
        window.location.href = "/"; //redirect to homepage
    });
}

function createRequest() {
  // Takes note id that we pass and it will send a post request to the delete note endpoint, and after it gets a response it will reload the window

  // Protocol
  let data = {}
  let select_e = document.getElementById("MajorSystemMode");
  let select_value = select_e.options[select_e.selectedIndex].value;
  data['protocol'] = select_value;
  
  select_e = document.getElementById("MinorMode");
  select_value = select_e.options[select_e.selectedIndex].value;
  data['mode'] = select_value;

  select_e = document.getElementById("DFI2CKRatio");
  select_value = select_e.options[select_e.selectedIndex].value;
  data['DFI2CKRatio'] = select_value;

  e = document.getElementById("baudRate");
  data['baud'] = e.value;

  console.log("data = ", data)

  console.log("Sending Request ...")
  fetch('/process_request', { // To send a request in vanilla js
    method: 'POST',
    body: JSON.stringify({data: data})  
  }).then((_res) => { // then reload the window
      console.log("Restarting Window ...");
      window.location.href = "/"; //redirect to homepage
  });
}


function downloadFile(req_idx) {
  // Takes note id that we pass and it will send a post request to the delete note endpoint, and after it gets a response it will reload the window
  console.log("req_idx = ", req_idx)
  fetch('/download', {
    method: 'POST',
    body: JSON.stringify({req_idx: req_idx})  
  }).then((_res) => { // then reload the window
      console.log("res = ", _res);
      // window.location.href = "/"; //redirect to homepage
  });

}