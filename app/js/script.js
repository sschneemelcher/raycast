function setup() {
	let cnv = createCanvas(1024, 512, P2D);
}

function drawLines(coordinates) {
	stroke(color(255,0,0));
	coordinates.forEach(function(current) {
		line(current[0], current[1], current[2], current[3])
		});
	}

function drawRects(rects) { // rects = [[x, y, w, h, "color"], [...],...]
	clear()
	rects.forEach(function(r) {
		fill(color(r[1][0],r[1][1],r[1][2]));
		noStroke();
		rect(r[0][0], r[0][1], r[0][2], r[0][3]);
		});
	}

function sendKey(e, v) {
	eel.move(e.keyCode, v)
}


eel.expose(setup);
eel.expose(drawLines);
eel.expose(drawRects);
