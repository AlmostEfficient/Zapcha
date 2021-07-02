console.log('Ready')

function displayImage(base64) {
    var image = document.getElementById("image")
    image.src = base64;
}

var endpoint = "http://172.24.252.112:5000/frame"

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
            console.log(data)
        });

}

getImage(endpoint)