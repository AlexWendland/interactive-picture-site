var socket = new WebSocket("ws://" + location.host + "/ws");

var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
var drawing = false;

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

function resizeImageSize() {
    const viewportWidth = window.innerWidth
    const viewportHeight = window.innerHeight;
    const viewportAspectRatio = viewportWidth / viewportHeight;

    // Image will change so we have to keep getting the natural size
    const img = document.getElementById('slideshow');
    const imgWidth = img.naturalWidth;
    const imgHeight = img.naturalHeight;
    const imgAspectRatio = imgWidth / imgHeight;

    if (imgAspectRatio > viewportAspectRatio) {
        // Image is wider relative to the viewport
        console.log("1");
        img.style.width = '100%';
        img.style.height = 'auto';
    } else {
        // Image is taller relative to the viewport
        console.log("2");
        img.style.width = 'auto';
        img.style.height = '100%';
    }
}

window.addEventListener('resize', resizeCanvas);
window.addEventListener('resize', resizeImageSize);
resizeCanvas();

socket.onmessage = function(event) {
    if (event.data.endsWith(".jpg") || event.data.endsWith(".png") || event.data.endsWith(".jpeg") || event.data.endsWith(".gif")) {
        document.getElementById('slideshow').src = '/static/images/' + event.data;
        console.log(event.data);
        resizeImageSize();
        // ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas for new image
    } else {
        var coords = JSON.parse(event.data);
        ctx.lineTo(coords.x, coords.y);
        ctx.stroke();
    }
};

canvas.addEventListener('mousedown', function(e) {
    drawing = true;
    ctx.moveTo(e.clientX, e.clientY);
});

canvas.addEventListener('mouseup', function() {
    drawing = false;
});

canvas.addEventListener('mousemove', function(e) {
    if (drawing) {
        ctx.lineTo(e.clientX, e.clientY);
        ctx.stroke();
        socket.send(JSON.stringify({x: e.clientX, y: e.clientY}));
    }
});
