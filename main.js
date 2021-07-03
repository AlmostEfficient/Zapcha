console.log('Ready')

function displayImage(base64) {
    var image = document.getElementById("image")
    image.src = base64;
}


// var endpoint = "http://172.24.252.112:5000/frame"
var endpoint = "http://192.168.0.72:5000/frame"
var selectedImages = [];

function getImage(endpoint) {
    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            var container = document.getElementById("container")

            data.forEach((element, idx) => {

                if (idx % 3 == 0) {
                    if (idx != 0) {
                        container.innerHTML += "</div>"
                    }
                    container.innerHTML += "<div class='image-row'>"
                }
                container.innerHTML += `<img class='image'src="data:image/jpg;base64,${element}">`
            });
            console.log("Added images from the server")
        });
    // setEvents()
}

getImage(endpoint)

function setEvents(){
    images = document.getElementsByClassName('image')
    images.forEach(element => {
        element.addEventListener("click", selectImage(this.id))
    });
    console.log("Added on click events.")
}

// Set in memory variable to indicate which images have been selected
function selectImage(id){
    // var id = this.id;
    if (selectedImages.includes(id)){
        var index = selectedImages.indexOf(id)
        console.log(`Unselected ${selectedImages[index]}`)
        selectedImages.pop(index)
    }
    else{
        selectedImages.push(id)
        console.log(`Selected ${selectedImages[index]}`)
    }
}

function submit(){
    payload = JSON.stringify(selectedImages)
    postData(endpoint, payload)
    .then(data => {
        console.log(data); // JSON data parsed by `data.json()` call
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
	return response.json(); // parses JSON response into native JavaScript objects
}