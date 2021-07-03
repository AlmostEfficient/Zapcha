console.log('Ready')

function displayImage(base64) {
    var image = document.getElementById("image")
    image.src = base64;
}


// var endpoint = "http://172.24.252.112:5000/frame"
var endpoint = "http://192.168.0.72:5000"
var selectedImages = {};

function getImage(endpoint) {
    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            var container = document.getElementById("container")
            let all_string = ""
            data.forEach((element, idx) => {
                selectedImages[idx] = false;
                if (idx % 3 == 0) {
                    if (idx != 0) {
                        all_string += "</div><div style='margin-top:-250px !important' class='image-row'>"
                    }else{
                        all_string += "<div class='image-row'>"

                    }
                }
                all_string += `<img onclick='onImageClick(${idx})' id='image-${idx}' class='image'src="data:image/jpg;base64,${element}">`
            });
            container.innerHTML += all_string;
            console.log("Added images from the server")
        });
}

getImage(endpoint+'/frame')
var selected = [];
function onImageClick(id){
    selectedImages[id] = !selectedImages[id];
    document.getElementById('image-'+id.toString()).style = "border: " + (selectedImages[id]==true ? "rgb(89, 156, 243)" : "white") +" solid 2px;";
    console.log(`Clicked ${id}`)
}

function submit(){
    console.log("Sending target data to server")
    payload = JSON.stringify(selectedImages)
    postData(endpoint+'/shoot', payload)
    .then(data => {

        data.json().then(result=>{
            console.log(result.response);
        }); // JSON data parsed by `data.json()` call
    });
}

async function postData(url = "", data = {}) {
	// Default options are marked with *
	const response = await fetch(url, {
		method: "POST", // *GET, POST, PUT, DELETE, etc.
		mode: "cors", // no-cors, *cors, same-origin
		cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
		credentials: "same-origin", // include, *same-origin, omit
		headers: {
			"Content-Type": "application/json",
			// 'Content-Type': 'application/x-www-form-urlencoded',
		},
		redirect: "follow", // manual, *follow, error
		referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
		body: JSON.stringify(data), // body data type must match "Content-Type" header
	});
	return response; 
}