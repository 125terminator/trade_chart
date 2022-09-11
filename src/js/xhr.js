export default function XHR(url) {
    let xhr = new XMLHttpRequest()
    xhr.onload = function() {
    if (xhr.status != 200) { // analyze HTTP status of the response
        console.log(`Error ${xhr.status}: ${xhr.statusText}`); // e.g. 404: Not Found
    } 
    // else { // show the result
    //     console.log(`Done, got ${xhr.response.length} bytes`); // response is the server response
    // }
    };
    xhr.onprogress = function(event) {
    if (event.lengthComputable) {
        console.log(`Received ${event.loaded} of ${event.total} bytes`);
    } else {
        console.log(`Received ${event.loaded} bytes`); // no Content-Length
    }
    };
    xhr.onerror = function() {
        console.log("Request failed");
        };

return {
    post(url, body) {
        xhr.open('POST', url)
        xhr.send(body)
    }
}
}
