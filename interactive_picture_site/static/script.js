var socket = new WebSocket("ws://" + location.host + "/ws");

var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
var drawing = false;

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

window.addEventListener('resize', resizeCanvas);
resizeCanvas();

socket.onmessage = function(event) {
    if (event.data.endsWith(".jpg") || event.data.endsWith(".png") || event.data.endsWith(".jpeg") || event.data.endsWith(".gif")) {
        document.getElementById('slideshow').src = '/static/images/' + event.data;
        ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas for new image
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
