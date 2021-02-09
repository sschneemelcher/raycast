function drawLines(coordinates) {
	var c = document.getElementById("myCanvas");
	var ctx = c.getContext("2d");
	ctx.strokeStyle = "red";
	coordinates.forEach(function(current) {
		ctx.moveTo(current[0], current[1]);
		ctx.lineTo(current[2], current[3]);
		ctx.stroke();
		});
	}

function drawRects(rects) { // rects = [[x, y, w, h, "color"], [...],...]
	var c = document.getElementById("myCanvas");
	var ctx = c.getContext("2d");
	ctx.beginPath();
	ctx.clearRect(0, 0, c.width, c.height);
	rects.forEach(function(rect) {
		ctx.fillStyle = "rgb("+rect[1][0]+","+rect[1][1]+","+rect[1][2]+")";
		ctx.fillRect(rect[0][0], rect[0][1], rect[0][2], rect[0][3]);
		});
	}

function sendKey(e, v) {
	eel.move(e.keyCode, v)
}

eel.expose(drawLines);
eel.expose(drawRects);
